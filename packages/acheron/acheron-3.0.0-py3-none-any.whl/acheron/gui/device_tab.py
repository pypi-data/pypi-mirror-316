from __future__ import annotations
import datetime
import functools
import io
import json
import logging
import lzma
import math
import multiprocessing.connection
import os
import pathlib
import platform
import struct
from typing import Any, cast, Optional, TYPE_CHECKING, Union
import weakref

import diskcache
import numpy
from numpy.typing import NDArray
from PySide6 import QtCore, QtGui, QtWidgets
import pyqtgraph

import asphodel
from asphodel import ChannelCalibration
from asphodel.device_info import DeviceInfo
import hyperborea.download
from hyperborea.unit_preferences import (get_default_option, get_unit_options,
                                         UnitOption)
from hyperborea.device_info_dialog import DeviceInfoDialog

from ..calc_process.types import ChannelInformation, LimitType
from ..core.calibration import get_channel_setting_values, update_nvm
from ..core.device_controller import DeviceController, DeviceControllerState
from ..core.preferences import Preferences
from ..device_logging import DeviceLoggerAdapter
from ..device_process import bootloader
from ..device_process.stream_controller import RFTestParams
from .calibration import CalibrationConnection, CalibrationPanel
from .change_stream_dialog import ChangeStreamDialog
from .connectivity_dialog import ConnectivityDialog
from .ctrl_var_panel import CtrlVarPanel
from .ctrl_var_widget import CtrlVarWidget
from .edit_alert_dialog import EditAlertDialog
from .gui_log import get_log_list_model
from .hardware_tests import HardwareTestDialog
from .led_control_widget import LEDControlWidget
from .radio_panel import RadioPanel
from .remote_panel import RemotePanel
from .rf_power_panel import RFPowerPanel
from .rf_test_dialog import RFTestDialog
from .rgb_control_widget import RGBControlWidget
from .setting_dialog import SettingDialog
from .ui.ui_device_tab import Ui_DeviceTab

if TYPE_CHECKING:
    from .plotmain import PlotMainWindow

logger = logging.getLogger(__name__)


class MeasurementLineEdit(QtWidgets.QLineEdit):
    def __init__(self, unit_actions: Optional[list[QtGui.QAction]],
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.unit_actions = unit_actions

        self.alert: bool = False

        self.setReadOnly(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight
                          | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                  QtWidgets.QSizePolicy.Policy.Minimum))
        self.setFixedWidth(100)

        self.copy_action = QtGui.QAction(self)
        self.copy_action.setText(self.tr("Copy Text"))
        self.copy_action.setShortcut(QtGui.QKeySequence.StandardKey.Copy)
        self.copy_action.setShortcutContext(
            QtCore.Qt.ShortcutContext.WidgetShortcut)
        self.copy_action.triggered.connect(self._copy_cb)
        self.addAction(self.copy_action)

        if self.unit_actions:
            self.separator = QtGui.QAction(self)
            self.separator.setSeparator(True)
            self.addAction(self.separator)
            self.addActions(self.unit_actions)

        self.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)

    @QtCore.Slot()
    def _copy_cb(self) -> None:
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.text())

    def set_alert(self, new_alert: bool) -> None:
        if new_alert and not self.alert:
            self.alert = True
            self.setStyleSheet("* { color: black; background-color: red; }")
        if self.alert and not new_alert:
            self.alert = False
            self.setStyleSheet("")


class EditAlertAction(QtGui.QAction):
    def __init__(self, channel_id: int, subchannel_index: int,
                 subchannel_name: str, device_tab: "DeviceTab",
                 parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.device_tab: "weakref.ReferenceType[DeviceTab]" = weakref.ref(
            device_tab)

        self.channel_id = channel_id
        self.subchannel_index = subchannel_index

        self.setText(self.tr("Edit Alert for {}").format(subchannel_name))
        self.triggered.connect(self.handle_edit)

    @QtCore.Slot()
    def handle_edit(self) -> None:
        device_tab = self.device_tab()
        if device_tab is None:
            return

        unit_option = device_tab.channel_unit.get(self.channel_id)
        if unit_option is None:
            return

        alert_limits = device_tab.controller.device_prefs.get_alert_limits(
            self.channel_id, self.subchannel_index)

        dialog = EditAlertDialog(
            alert_limits, unit_option.unit_formatter, device_tab)
        try:
            ret = dialog.exec()
            if ret == 0:
                return  # user cancelled

            alert_limits = dialog.get_alert_limits()
        finally:
            dialog.deleteLater()

        device_tab.controller.device_prefs.set_alert_limits(
            self.channel_id, self.subchannel_index, alert_limits)

        device_tab.controller.update_preferences()
        device_tab.update_alert_action_icons()


class DeviceTab(Ui_DeviceTab, QtWidgets.QWidget):
    collapsed_set = QtCore.Signal(bool)

    def __init__(self, controller: DeviceController, plotmain: PlotMainWindow,
                 preferences: Preferences, collapsed: bool,
                 firmware_cache: diskcache.Cache,
                 tree_item: QtWidgets.QTreeWidgetItem) -> None:
        super().__init__(None)

        self.controller = controller
        self.plotmain = plotmain
        self.preferences = preferences
        self.collapsed = collapsed
        self.firmware_cache = firmware_cache
        self.tree_item = tree_item

        self.settings = QtCore.QSettings()

        # create a logger that includes the serial number information
        self.logger = DeviceLoggerAdapter(
            logger, self.controller.serial_number)

        # keys: channel_id
        self.subchannel_fields: dict[
            int, list[tuple[MeasurementLineEdit, MeasurementLineEdit]]] = {}
        self.channel_unit_options: dict[int, list[UnitOption]] = {}
        self.channel_unit_actions: dict[int, list[QtGui.QAction]] = {}
        self.channel_unit_action_group: dict[int, QtGui.QActionGroup] = {}
        self.channel_unit_type: dict[int, int] = {}
        self.channel_unit_default: dict[int, UnitOption] = {}
        self.channel_unit: dict[int, UnitOption] = {}
        self.channel_alert_actions: dict[int, list[QtGui.QAction]] = {}

        self.rgb_widgets: list[RGBControlWidget] = []
        self.led_widgets: list[LEDControlWidget] = []
        self.ctrl_var_widgets: list[CtrlVarWidget] = []
        self.calibration_panel: Optional[CalibrationPanel] = None
        self.calibration_cals: list[CalibrationConnection] = []
        self.shaker_id: Optional[int] = None
        self.shaker_calibration_info: Optional[ChannelCalibration] = None

        self.combo_box_channel_ids: list[int] = []
        self.last_channel_id = None  # last plotted channel
        self.last_plot_range_channel_id = None  # last loaded plot range

        self.saved_plot_ranges: dict[int, dict] = {}

        # k: channel_id, v: (mean, std)
        self.channel_data: dict[
            int, tuple[NDArray[numpy.float64], NDArray[numpy.float64]]] = {}

        self.lost_packet_count = 0
        self.lost_packet_last_time = None
        self.recent_lost_packet_highlight = False
        self.last_displayed_packet_count = 0
        self.last_displayed_packet_time = None

        self.time_curves: list[pyqtgraph.PlotDataItem] = []
        self.legend = None

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup()
        self.setup_logging()
        self.setup_callbacks()
        self.setup_graphics()

        # update the state now
        self.controller_state_changed(self.controller.state,
                                      self.tr("Connecting"))
        self._manual_control_changed_cb(self.controller.get_manual_control())

    def extra_ui_setup(self) -> None:
        # make status label visible (this is easily forgotten in QtDesigner)
        self.stackedWidget.setCurrentIndex(0)

        # hide status progress bar
        self.statusProgressBar.setVisible(False)

        # clear out the labels
        self.serialNumber.setText(self.controller.serial_number)
        self.userTag1.setText("")
        self.userTag2.setText("")
        self.boardInfo.setText("")
        self.buildInfo.setText("")
        self.buildDate.setText("")
        self.branch.setText("")
        self.bootloaderIndicator.setVisible(False)
        self.nvmModifiedIndicator.setVisible(False)

        self.schedule_or_trigger_count_updated()

        self.menu = QtWidgets.QMenu()
        self.firmware_menu = self.menu.addMenu(self.tr("Update Firmware"))
        self.firmware_menu.setEnabled(False)
        self.firmware_menu.addAction(self.actionFirmwareLatestStable)
        self.firmware_menu.addAction(self.actionFirmwareFromBranch)
        self.firmware_menu.addAction(self.actionFirmwareFromCommit)
        self.firmware_menu.addAction(self.actionFirmwareFromFile)
        self.advanced_menu = self.menu.addMenu(self.tr("Advanced Actions"))
        self.advanced_menu.addAction(self.actionForceRunBootloader)
        self.advanced_menu.addAction(self.actionForceRunApplication)
        self.advanced_menu.addAction(self.actionForceReset)
        self.advanced_menu.addAction(self.actionRaiseException)
        self.advanced_menu.addAction(self.actionRecoverNVM)
        self.menu.addSeparator()
        self.menu.addAction(self.actionCalibrate)
        self.menu.addAction(self.actionShakerCalibrate)
        self.menu.addSeparator()
        self.menu.addAction(self.actionConnectivity)
        self.actionRFTestSeparator = self.menu.addSeparator()
        self.menu.addAction(self.actionRFTest)
        self.menu.addSeparator()
        self.menu.addAction(self.actionSetDeviceMode)
        self.menu.addAction(self.actionChangeActiveStreams)
        self.menu.addAction(self.actionRunTests)
        self.menuButton.setMenu(self.menu)

        self.actionCalibrate.setIcon(QtGui.QIcon.fromTheme("caliper"))
        self.actionChangeActiveStreams.setIcon(
            QtGui.QIcon.fromTheme("preferences_edit"))
        self.actionConnectivity.setIcon(
            QtGui.QIcon.fromTheme("client_network"))
        self.actionEditDeviceSettings.setIcon(QtGui.QIcon.fromTheme("gear"))
        self.actionFirmwareFromBranch.setIcon(
            QtGui.QIcon.fromTheme("branch_view"))
        self.actionFirmwareFromCommit.setIcon(
            QtGui.QIcon.fromTheme("symbol_hash"))
        self.actionFirmwareFromFile.setIcon(
            QtGui.QIcon.fromTheme("document_plain"))
        self.actionFirmwareLatestStable.setIcon(
            QtGui.QIcon.fromTheme("branch"))
        self.actionForceReset.setIcon(QtGui.QIcon.fromTheme("redo"))
        self.actionForceRunApplication.setIcon(
            QtGui.QIcon.fromTheme("application"))
        self.actionForceRunBootloader.setIcon(
            QtGui.QIcon.fromTheme("flash_yellow"))
        self.actionRaiseException.setIcon(QtGui.QIcon.fromTheme("bomb"))
        self.actionRecoverNVM.setIcon(QtGui.QIcon.fromTheme("document_gear"))
        self.actionRFTest.setIcon(QtGui.QIcon.fromTheme("rf_test"))
        self.actionRunTests.setIcon(QtGui.QIcon.fromTheme("stethoscope"))
        self.actionSetDeviceMode.setIcon(
            QtGui.QIcon.fromTheme("text_list_numbers"))
        self.actionCopySerialNumber.setIcon(QtGui.QIcon.fromTheme("copy"))
        self.actionSetUserTag1.setIcon(QtGui.QIcon.fromTheme("tag"))
        self.actionSetUserTag2.setIcon(QtGui.QIcon.fromTheme("tag"))
        self.actionShakerCalibrate.setIcon(QtGui.QIcon.fromTheme("shaker"))
        self.actionShowDeviceInfo.setIcon(QtGui.QIcon.fromTheme("information"))
        self.actionFlushLostPackets.setIcon(QtGui.QIcon.fromTheme("replace2"))
        self.actionShowPacketStats.setIcon(
            QtGui.QIcon.fromTheme("chart_column"))
        self.firmware_menu.setIcon(QtGui.QIcon.fromTheme("cpu_flash"))
        self.advanced_menu.setIcon(QtGui.QIcon.fromTheme("wrench"))

        # firmware flash/download progress dialog
        self.firmware_progress = QtWidgets.QProgressDialog("", "", 0, 100)
        self.firmware_progress.setLabelText(self.tr(""))
        self.firmware_progress.setWindowTitle(self.tr("Firmware Update"))
        self.firmware_progress.setCancelButton(None)  # type: ignore
        self.firmware_progress.setWindowModality(
            QtCore.Qt.WindowModality.WindowModal)
        self.firmware_progress.setMinimumDuration(0)
        self.firmware_progress.setAutoReset(False)
        self.firmware_progress.reset()

        # set collapse to known state
        self.set_collapsed(self.collapsed)

        self.deviceInfo.setDefaultAction(self.actionShowDeviceInfo)
        self.copySerialNumber.setDefaultAction(self.actionCopySerialNumber)
        self.setUserTag1.setDefaultAction(self.actionSetUserTag1)
        self.setUserTag2.setDefaultAction(self.actionSetUserTag2)
        self.flushLostPackets.setDefaultAction(self.actionFlushLostPackets)
        self.lostPacketDetails.setDefaultAction(self.actionShowPacketStats)
        self.editDeviceSettings.setDefaultAction(self.actionEditDeviceSettings)

        # create all of the panels
        self.ctrl_var_panel = CtrlVarPanel(self)
        self.panelLayout.addWidget(self.ctrl_var_panel)

        self.rf_power_panel = RFPowerPanel(self.controller, self)
        self.panelLayout.addWidget(self.rf_power_panel)

        self.radio_panel = RadioPanel(
            self.controller, self.plotmain.dispatcher.active_scan_database,
            self.preferences, self)
        self.radio_panel.show_remote_clicked.connect(self.show_remote_tab)
        self.panelLayout.addWidget(self.radio_panel)

        self.remote_panel = RemotePanel(self)
        self.remote_panel.show_radio_clicked.connect(self.show_radio_tab)
        self.panelLayout.addWidget(self.remote_panel)

        # update the trigger display
        inactive_triggers = self.controller.trigger_names.difference(
            self.controller.last_emitted_active_triggers)
        self.active_triggers_changed_cb(
            self.controller, self.controller.last_emitted_active_triggers,
            inactive_triggers)

    def setup_callbacks(self) -> None:
        self.closeButton.clicked.connect(self.close_controller)

        self.graphChannelComboBox.currentIndexChanged.connect(
            self.graph_channel_changed)
        self.fftSubchannelComboBox.currentIndexChanged.connect(
            self.fft_subchannel_changed)

        self.actionCopySerialNumber.triggered.connect(self.copy_serial_number)
        self.actionSetUserTag1.triggered.connect(self.set_user_tag_1)
        self.actionSetUserTag2.triggered.connect(self.set_user_tag_2)
        self.actionFirmwareLatestStable.triggered.connect(
            self.do_bootloader_latest_stable)
        self.actionFirmwareFromBranch.triggered.connect(
            self.do_bootloader_from_branch)
        self.actionFirmwareFromCommit.triggered.connect(
            self.do_bootloader_from_commit)
        self.actionFirmwareFromFile.triggered.connect(
            self.do_bootloader_from_file)
        self.actionForceRunBootloader.triggered.connect(
            self.controller.force_run_bootloader)
        self.actionForceRunApplication.triggered.connect(
            self.controller.force_run_application)
        self.actionForceReset.triggered.connect(self.controller.force_reset)
        self.actionRaiseException.triggered.connect(self.controller.do_explode)
        self.actionRecoverNVM.triggered.connect(self.recover_nvm)
        self.actionFlushLostPackets.triggered.connect(self.flush_lost_packets)
        self.actionShowPacketStats.triggered.connect(self.show_packet_stats)
        self.actionChangeActiveStreams.triggered.connect(
            self.change_active_streams)
        self.actionShowDeviceInfo.triggered.connect(self.show_device_info)
        self.actionCalibrate.triggered.connect(self.calibrate)
        self.actionShakerCalibrate.triggered.connect(self.shaker_calibrate)
        self.actionConnectivity.triggered.connect(
            self.show_connectivity_dialog)
        self.actionRFTest.triggered.connect(self.rf_test)
        self.actionEditDeviceSettings.triggered.connect(self.edit_settings)
        self.actionRunTests.triggered.connect(self.run_tests)
        self.actionSetDeviceMode.triggered.connect(self.set_device_mode)

        self.collapseButton.clicked.connect(self.toggle_collapsed)

        self.controller.state_changed_signal.connect(
            self.controller_state_changed)
        self.controller.progress_signal.connect(self.progress_update)

        self.controller.channel_update.connect(self.channel_update_cb)
        self.controller.plot_update.connect(self.plot_update_cb)
        self.controller.fft_update.connect(self.fft_update_cb)
        self.controller.lost_packet_update.connect(self.lost_packet_update)

        self.controller.rgb_updated.connect(self.rgb_updated_cb)
        self.controller.led_updated.connect(self.led_updated_cb)
        self.controller.ctrl_var_updated.connect(self.ctrl_var_updated_cb)

        self.controller.alerts_changed.connect(self.alerts_changed_cb)

        self.controller.manual_control_changed.connect(
            self._manual_control_changed_cb)

        self.controller.trigger_count_changed.connect(
            self.schedule_or_trigger_count_updated)
        self.controller.schedule_count_changed.connect(
            self.schedule_or_trigger_count_updated)

        self.controller.active_triggers_changed.connect(
            self.active_triggers_changed_cb)

        self.firmware_finder = hyperborea.download.FirmwareFinder(self.logger)
        self.firmware_finder.completed.connect(self.firmware_finder_completed)
        self.firmware_finder.error.connect(self.firmware_finder_error)
        self.ref_finder = hyperborea.download.RefFinder(self.logger)
        self.ref_finder.completed.connect(self.ref_finder_completed)
        self.ref_finder.error.connect(self.ref_finder_error)
        self.downloader = hyperborea.download.Downloader(self.logger)
        self.downloader.completed.connect(self.download_completed)
        self.downloader.error.connect(self.download_error)
        self.downloader.update.connect(self.download_update_progress)

    def update_preferences(self) -> None:
        show_rf_test = self.preferences.show_rf_test
        self.actionRFTestSeparator.setVisible(show_rf_test)
        self.actionRFTest.setVisible(show_rf_test)

        device_info = self.controller.device_info
        if device_info:
            self.update_supply_display(device_info)

        for channel_id, unit_options in self.channel_unit_options.items():
            unit_type = self.channel_unit_type[channel_id]
            new_default = get_default_option(
                self.settings, unit_type, unit_options)
            old_default = self.channel_unit_default[channel_id]
            if new_default != old_default:
                if old_default == self.channel_unit[channel_id]:
                    # update current choice
                    self.channel_unit[channel_id] = new_default
                    index = unit_options.index(new_default)
                    action = self.channel_unit_actions[channel_id][index]
                    action.setChecked(True)

                # update the default
                self.channel_unit_default[channel_id] = new_default

        self.update_alert_action_icons()

        self.graph_channel_changed()

    def setup_logging(self) -> None:
        # create a model for the logList
        self.log_list_model = get_log_list_model(self.controller.serial_number)
        self.log_list_model.dataChanged.connect(self.log_list_updated)
        self.logList.setModel(self.log_list_model)
        self.logListDisconnected.setModel(self.log_list_model)
        self.log_selection_model = QtCore.QItemSelectionModel(
            self.log_list_model)
        self.logList.setSelectionModel(self.log_selection_model)
        self.logListDisconnected.setSelectionModel(self.log_selection_model)

        # hide the disconnected page's log when there's nothing visible
        self.logListDisconnected.setVisible(False)

        # copy action for log list
        self.logList.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
        self.logListDisconnected.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
        self.copy_log_action = QtGui.QAction()
        self.copy_log_action.setText(self.tr("Copy"))
        self.copy_log_action.setShortcut(QtGui.QKeySequence.StandardKey.Copy)
        self.copy_log_action.setShortcutContext(
            QtCore.Qt.ShortcutContext.WidgetShortcut)
        self.copy_log_action.triggered.connect(self._copy_log_cb)
        self.logList.addAction(self.copy_log_action)
        self.logListDisconnected.addAction(self.copy_log_action)

        # synchronize the scroll bars between the two log widgets
        sb1 = self.logList.verticalScrollBar()
        sb2 = self.logListDisconnected.verticalScrollBar()
        sb1.valueChanged.connect(sb2.setValue)
        sb2.valueChanged.connect(sb1.setValue)

    @QtCore.Slot()
    def log_list_updated(self) -> None:
        # check if the scroll window is already at the bottom
        sb1 = self.logList.verticalScrollBar()
        sb2 = self.logListDisconnected.verticalScrollBar()
        at_bottom = (sb1.value() == sb1.maximum() or
                     sb2.value() == sb2.maximum())

        # have a log message now
        self.logListDisconnected.setVisible(True)

        # adjust the scroll position if necessary
        if at_bottom:
            self.logListDisconnected.scrollToBottom()
            self.logList.scrollToBottom()

    @QtCore.Slot()
    def _copy_log_cb(self) -> None:
        clipboard = QtWidgets.QApplication.clipboard()
        indexes = self.logList.selectedIndexes()
        text = "\n".join([i.data() for i in indexes])
        if text:
            clipboard.setText(text)

    def setup_graphics(self) -> None:
        fft_pen = "c"

        self.timePlot: pyqtgraph.PlotItem = \
            self.timePlotWidget.getPlotItem()  # type: ignore
        self.fftPlot: pyqtgraph.PlotItem = \
            self.fftPlotWidget.getPlotItem()  # type: ignore

        # this is just to help the type annotation
        assert isinstance(self.timePlot, pyqtgraph.PlotItem)
        assert isinstance(self.fftPlot, pyqtgraph.PlotItem)

        self.timePlot.showGrid(x=True, y=True)
        self.fftPlot.showGrid(x=True, y=True)

        self.timePlot.setLabel("bottom", "Time (s)")
        self.fftPlot.setLabel("bottom", "Frequency (Hz)")

        self.timePlot.setTitle("Time Domain")
        self.fftPlot.setTitle("Frequency Domain")

        self.bufferingLabel = pyqtgraph.LabelItem("Buffering", size="12pt")
        self.bufferingLabel.setParentItem(self.fftPlot.graphicsItem())
        self.bufferingLabel.anchor(itemPos=(0.5, 0.5), parentPos=(0.5, 0.5))
        self.bufferingLabel.setVisible(False)
        self.buffering = False

        self.noChannelsTimeLabel = pyqtgraph.LabelItem("No Channels",
                                                       size="12pt")
        self.noChannelsTimeLabel.setParentItem(self.timePlot.graphicsItem())
        self.noChannelsTimeLabel.anchor(itemPos=(0.5, 0.5),
                                        parentPos=(0.5, 0.5))
        self.noChannelsTimeLabel.setVisible(False)
        self.noChannelsFreqLabel = pyqtgraph.LabelItem("No Channels",
                                                       size="12pt")
        self.noChannelsFreqLabel.setParentItem(self.fftPlot.graphicsItem())
        self.noChannelsFreqLabel.anchor(itemPos=(0.5, 0.5),
                                        parentPos=(0.5, 0.5))
        self.noChannelsFreqLabel.setVisible(False)

        self.fft_curve = self.fftPlot.plot(pen=fft_pen)

        axes = []
        for name in ('top', 'bottom', 'left', 'right'):
            axes.append(self.timePlot.getAxis(name))
            axes.append(self.fftPlot.getAxis(name))

        for axis in axes:
            axis.setZValue(-1000)
            axis.setStyle(autoReduceTextSpace=False)

        def override_label_string(axis: pyqtgraph.AxisItem) -> None:
            old_method = axis.labelString

            def new_func(self: Any) -> str:
                # take off the leading <span>
                s = old_method()
                i = s.find(">")
                prefix = s[:i + 1]
                s = s[i + 1:]
                # take off the trailing </span>
                i = s.rfind("<")
                suffix = s[i:]
                s = s[:i]
                s = s.strip()
                if s.startswith("(") and s.endswith(")"):
                    s = s.strip("()")
                return "".join((prefix, s, suffix))

            new_method = new_func.__get__(axis)
            axis.labelString = new_method

        override_label_string(self.timePlot.getAxis("left"))
        override_label_string(self.fftPlot.getAxis("left"))

    def update_supply_display(self, device_info: DeviceInfo) -> None:
        supply_strings = []
        battery_strings = []
        supplies = device_info.supplies
        for i, (_name, supply) in enumerate(supplies):
            supply_results = device_info.supply_results[i]
            if supply_results is not None:
                value, result_flags = supply_results
                scaled_value = value * supply.scale + supply.offset
                formatted = asphodel.format_value_ascii(
                    supply.unit_type, supply.scale, scaled_value)
                if result_flags == 0:
                    # ok
                    good_result = True
                    result_string = formatted
                elif result_flags == asphodel.ASPHODEL_SUPPLY_LOW_BATTERY:
                    # low batt
                    good_result = False
                    result_string = ('<span style="background-color: yellow; '
                                     f'color: black;">{formatted}</span>')
                else:
                    # fail
                    good_result = False
                    result_string = ('<span style="background-color: red; '
                                     f'color: black;">{formatted}</span>')

                if supply.is_battery:
                    # show regardless
                    battery_strings.append(result_string)
                else:
                    # show if relevant
                    if not good_result:
                        supply_strings.append(result_string)

        if battery_strings:
            self.battery.setText(", ".join(battery_strings))
            self.battery.setVisible(True)
            self.batteryLabel.setVisible(True)
        else:
            self.battery.setVisible(False)
            self.batteryLabel.setVisible(False)

        if self.preferences.show_supplies and supply_strings:
            self.supplies.setText(", ".join(supply_strings))
            self.supplies.setVisible(True)
            self.suppliesLabel.setVisible(True)
        else:
            self.supplies.setVisible(False)
            self.suppliesLabel.setVisible(False)

    @QtCore.Slot()
    def toggle_collapsed(self) -> None:
        new_collapsed = not self.collapsed
        # NOTE: don't need to call self.set_collapsed() directly
        self.collapsed_set.emit(new_collapsed)

    def set_collapsed(self, collapsed: bool) -> None:
        self.collapsed = collapsed

        if collapsed:
            self.collapseButton.setText(self.tr("\u25B2 Expand \u25B2"))
        else:
            self.collapseButton.setText(self.tr("\u25BC Collapse \u25BC"))
        self.bottomGroup.setVisible(not collapsed)

    @QtCore.Slot()
    def copy_serial_number(self) -> None:
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.controller.serial_number)

    @QtCore.Slot()
    def set_user_tag_1(self) -> None:
        self.set_user_tag(0)

    @QtCore.Slot()
    def set_user_tag_2(self) -> None:
        self.set_user_tag(1)

    def set_user_tag(self, index: int) -> None:
        if not self.controller.device_info:
            # not connected
            return

        # find the current setting
        tag_key = "user_tag_" + str(index + 1)
        old_str = getattr(self.controller.device_info, tag_key)

        # ask the user for the new string
        new_str, ok = QtWidgets.QInputDialog.getText(
            self, self.tr("New Tag"), self.tr("New Tag:"),
            QtWidgets.QLineEdit.EchoMode.Normal, old_str)

        if not ok:
            return

        new_str = new_str.strip()

        self.controller.set_user_tag(index, new_str)

    @QtCore.Slot()
    def recover_nvm(self) -> None:
        if not self.controller.device_info:
            # not connected
            return

        current_length = len(self.controller.device_info.nvm)

        # ask the user for the file name
        apd_dir = self.preferences.base_dir
        caption = self.tr("Open Data File")
        file_filter = self.tr("Data Files (*.apd);;All Files (*.*)")
        val = QtWidgets.QFileDialog.getOpenFileName(self, caption, apd_dir,
                                                    file_filter)
        filename = val[0]
        if filename == "":
            return

        # open file and decompress
        fp = lzma.open(filename, 'rb')

        # read the header from the file
        leader_bytes: bytes = fp.read(12)  # type: ignore
        header_leader = struct.unpack(">dI", leader_bytes)
        header_bytes: bytes = fp.read(header_leader[1])  # type: ignore
        header_str = header_bytes.decode("UTF-8")
        header = json.loads(header_str)
        new_nvm = bytes.fromhex(header['nvm'])

        # check the nvm lengths
        new_length = len(new_nvm)
        if new_length != current_length:
            # need to add a popup here #
            message = self.tr("NVM sizes do not match!")
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), message)
            return

        # write the nvm
        self.controller.write_nvm(new_nvm)

    @QtCore.Slot()
    def flush_lost_packets(self) -> None:
        self.controller.reset_lost_packets()

        # update UI
        self.recentLostPackets.setText(str(0))
        if self.recent_lost_packet_highlight:
            self.recent_lost_packet_highlight = False
            self.recentLostPackets.setStyleSheet("")

    @QtCore.Slot()
    def show_packet_stats(self) -> None:
        count_since_last = (self.lost_packet_count -
                            self.last_displayed_packet_count)
        self.last_displayed_packet_count = self.lost_packet_count

        now = datetime.datetime.now(tz=datetime.timezone.utc)

        if self.last_displayed_packet_time is not None:
            last_check_str = self.last_displayed_packet_time.strftime(
                "%Y-%m-%dT%H:%M:%SZ")  # use ISO 8601 representation
        else:
            last_check_str = self.tr("Never")
        self.last_displayed_packet_time = now

        if self.lost_packet_last_time is not None:
            delta = now - self.lost_packet_last_time

            # remove microseconds
            delta = delta - datetime.timedelta(microseconds=delta.microseconds)
            last_loss_str = str(delta)
        else:
            last_loss_str = self.tr("N/A")

        msg = (f"All Time Lost Packets: {self.lost_packet_count}\n"
               f"Time since last packet loss: {last_loss_str}\n"
               f"Lost Since Last Check: {count_since_last}\n"
               f"Time of last check: {last_check_str}")

        QtWidgets.QMessageBox.information(self, self.tr("Packet Loss Stats"),
                                          msg)

    @QtCore.Slot(object, object, object)
    def lost_packet_update(self, total: int,
                           last_datetime: Optional[datetime.datetime],
                           recent: int) -> None:
        self.lost_packet_count = total
        self.lost_packet_last_time = last_datetime

        self.recentLostPackets.setText(str(recent))
        if recent > 0:
            if not self.recent_lost_packet_highlight:
                self.recent_lost_packet_highlight = True
                self.recentLostPackets.setStyleSheet(
                    "* { color: black; background-color: red }")
        else:
            if self.recent_lost_packet_highlight:
                self.recent_lost_packet_highlight = False
                self.recentLostPackets.setStyleSheet("")

    @QtCore.Slot()
    def change_active_streams(self) -> None:
        if not self.controller.device_info:
            return

        dialog = ChangeStreamDialog(
            self.controller.device_info.streams,
            self.controller.device_info.channels,
            self.controller.active_streams, self)
        try:
            ret = dialog.exec()
            if ret == 0:
                return  # user cancelled

            stream_list = dialog.get_new_stream_list()
        finally:
            dialog.deleteLater()

        self.controller.set_active_streams(stream_list)

    @QtCore.Slot()
    def show_connectivity_dialog(self) -> None:
        if not self.controller.device_info:
            return

        dialog = ConnectivityDialog(
            self.controller.serial_number, self.controller.device_info,
            self.controller.channel_info, self.controller.device_prefs, self)
        try:
            ret = dialog.exec()
            if ret == 0:
                return  # user cancelled
        finally:
            dialog.deleteLater()

        self.update_preferences()
        self.controller.update_preferences()

        self.controller.start_connectivity()

    @QtCore.Slot()
    def show_device_info(self) -> None:
        if self.controller.device_info:
            dialog = DeviceInfoDialog(self.controller.device_info, self)
            try:
                dialog.exec()
            finally:
                dialog.deleteLater()

    @QtCore.Slot()
    def run_tests(self) -> None:
        if self.controller.device_info:
            dialog = HardwareTestDialog(
                self.controller.device_info, self.controller, self.preferences,
                self.logger, self)
            try:
                dialog.start_tests()
                dialog.exec()
            finally:
                dialog.deleteLater()

    @QtCore.Slot()
    def set_device_mode(self) -> None:
        if self.controller.device_info:
            old_mode = self.controller.device_info.device_mode
            if old_mode is None:
                old_mode = 0
        else:
            old_mode = 0

        new_mode, ok = QtWidgets.QInputDialog.getInt(
            self, self.tr("Device Mode"), self.tr("Input new device mode"),
            old_mode, 0, 255)
        if not ok:
            return
        self.controller.set_device_mode(new_mode)

    @QtCore.Slot()
    def calibrate(self) -> None:
        if not self.controller.device_info:
            return

        if self.calibration_panel is None:
            self.calibration_panel = CalibrationPanel(
                self.controller.device_info, self.calibration_cals.copy(),
                self.logger, self.controller.write_nvm,
                self.plotmain.dispatcher.event_uploader)
            manual_control = self.controller.get_manual_control()
            self.calibration_panel.setEnabled(manual_control)
            self.panelLayout.insertWidget(0, self.calibration_panel)

        if self.actionCalibrate.isChecked():
            # start
            self.actionCalibrate.setText(self.tr("Stop Calibration"))
            self.calibration_panel.setVisible(True)
        else:
            # stop
            self.actionCalibrate.setText(self.tr("Start Calibration"))
            self.calibration_panel.setVisible(False)

    @QtCore.Slot()
    def rf_test(self) -> None:
        dialog = RFTestDialog(self)
        try:
            ret = dialog.exec()
            if ret == 0:
                return  # user cancelled

            test_params = dialog.get_test_params()
        finally:
            dialog.deleteLater()

        finished_rx_pipe, finished_tx_pipe = multiprocessing.Pipe(False)
        params = RFTestParams(
            test_params,
            cast(multiprocessing.connection.Connection, finished_rx_pipe)
        )
        self.controller.start_rf_test(params)

        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle(self.tr("RF Test"))
        msg_box.setText(self.tr("Running RF Test"))
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Abort)

        button = msg_box.button(QtWidgets.QMessageBox.StandardButton.Abort)
        button.setText(self.tr("Stop"))

        self.controller.rf_test_finished.connect(msg_box.reject)
        msg_box.exec()

        # let the stream controller know to stop the test
        finished_tx_pipe.send(None)

    @QtCore.Slot()
    def edit_settings(self) -> None:
        if not self.controller.device_info:
            return

        dialog = SettingDialog(self.controller.device_info, self)
        try:
            ret = dialog.exec()
            if ret == 0:
                return  # user cancelled

            try:
                new_nvm = dialog.get_updated_nvm()
            except Exception:
                self.logger.exception("Unhandled Exception in edit_settings")
                QtWidgets.QMessageBox.critical(
                    self, self.tr("Error"), self.tr("Error parsing settings!"))
                return
        finally:
            dialog.deleteLater()

        self.controller.write_nvm(new_nvm)

    def capture_func(self, channel_id: int) -> tuple[
            NDArray[numpy.float64], NDArray[numpy.float64]]:
        try:
            mean, std_dev = self.channel_data[channel_id]
            return (mean, std_dev)
        except KeyError:
            nanarray = numpy.array([[numpy.nan]])
            return (nanarray, nanarray)

    @QtCore.Slot()
    def shaker_calibrate(self) -> None:
        device_info = self.controller.device_info
        if not device_info:
            self.logger.error("No device information for shaker calibration")
            return

        if self.shaker_calibration_info is None or self.shaker_id is None:
            self.logger.error("Invalid state for shaker calibration")
            return

        ret = QtWidgets.QMessageBox.information(
            self, self.tr("Calibration"),
            self.tr("Let the shaker run for at least 1 second, "
                    "then press Ok."),
            QtWidgets.QMessageBox.StandardButton.Ok |
            QtWidgets.QMessageBox.StandardButton.Cancel)

        if ret != QtWidgets.QMessageBox.StandardButton.Ok:
            return

        settings = device_info.settings
        unit_type = asphodel.UNIT_TYPE_M_PER_S2
        cal = self.shaker_calibration_info

        mean, std_dev = self.capture_func(self.shaker_id)

        try:
            mean_value = mean.item()
            std_dev_value = std_dev.item()

            unscaled_mag = std_dev_value / cal.scale
            unscaled_offset = (mean_value - cal.offset) / cal.scale

            scale = 9.80665 / unscaled_mag

            if scale == 0:
                raise ValueError("Invalid scale")

            offset = -unscaled_offset * scale
        except Exception:
            msg = "Error performing calibration"
            self.logger.exception(msg)
            QtWidgets.QMessageBox.critical(self, self.tr("Error"),
                                           self.tr(msg))
            return

        event_data = {
            "board_type": device_info.board_info[0],
            "board_rev": device_info.board_info[1],
            "computer": platform.node(),
            "calibration_type": "Shaker",
            "scale": scale,
            "offset": offset,
        }

        u, f = get_channel_setting_values(len(settings), cal, unit_type, scale,
                                          offset)
        new_nvm = update_nvm(device_info.nvm, settings, u, f,
                             self.logger)

        self.controller.write_nvm(new_nvm)
        self.plotmain.dispatcher.event_uploader.calibration_finished(
            self.controller.serial_number, event_data)

    def create_calibration_info(self, device_info: DeviceInfo,
                                manual_control: bool) -> None:
        if self.calibration_panel:
            self.panelLayout.removeWidget(self.calibration_panel)
            self.calibration_panel.deleteLater()
            self.calibration_panel = None

        self.calibration_cals.clear()

        channel_calibration = device_info.channel_calibration
        for channel_id, calibration_info in enumerate(channel_calibration):
            if calibration_info is not None:
                channel_info = self.controller.channel_info.get(channel_id)
                if channel_info:
                    # setup variables to be used by the shaker calibration
                    # (only available if there is exactly one channel)
                    self.shaker_id = channel_id
                    self.shaker_calibration_info = calibration_info

                    uf = self.channel_unit[channel_id].unit_formatter
                    self.calibration_cals.append(CalibrationConnection(
                        name=channel_info.name,
                        calibration_info=calibration_info,
                        channel_id=channel_id,
                        device_tab=weakref.ref(self),
                        unit_formatter=uf)
                    )

        self.actionCalibrate.setEnabled((len(self.calibration_cals) > 0)
                                        and manual_control)

        if len(self.calibration_cals) == 1:
            self.actionShakerCalibrate.setEnabled(manual_control)
        else:
            self.shaker_id = None
            self.shaker_calibration_info = None

        # clean up old stuff
        self.actionCalibrate.setChecked(False)
        self.actionCalibrate.setText(self.tr("Start Calibration"))

    @QtCore.Slot(object, object, object)
    def channel_update_cb(self, channel_id: int, mean: NDArray[numpy.float64],
                          std_dev: NDArray[numpy.float64]) -> None:
        self.channel_data[channel_id] = (mean, std_dev)
        unit_formatter = self.channel_unit[channel_id].unit_formatter

        mean_scaled = (mean * unit_formatter.conversion_scale +
                       unit_formatter.conversion_offset)
        std_dev_scaled = std_dev * unit_formatter.conversion_scale

        for i, fields in enumerate(self.subchannel_fields[channel_id]):
            # update the text boxes
            mean_field, std_dev_field = fields
            mean_string = unit_formatter.format_utf8(mean_scaled[i])
            mean_field.setText(mean_string)
            std_dev_string = unit_formatter.format_utf8(std_dev_scaled[i])
            std_dev_field.setText(std_dev_string)

    @QtCore.Slot(object, object, object)
    def plot_update_cb(self, channel_id: int, time: NDArray[numpy.float64],
                       data: NDArray[numpy.float64]) -> None:
        selected_channel_id = self.get_current_channel_id()
        if channel_id != selected_channel_id:
            # old data
            return

        try:
            channel_info = self.controller.channel_info[channel_id]
        except KeyError:
            # disconnect in progress
            return

        if self.last_channel_id != channel_id:
            self.last_channel_id = channel_id
            if channel_info.downsample_factor == 1:
                self.timePlot.setTitle("Time Domain")
            else:
                s = "Time Domain (Downsampled {}x)".format(
                    channel_info.downsample_factor)
                self.timePlot.setTitle(s)

        # apply unit conversions
        unit_formatter = self.channel_unit[channel_id].unit_formatter
        data = (data * unit_formatter.conversion_scale +
                unit_formatter.conversion_offset)

        for array, curve in zip(data.transpose(), self.time_curves):
            curve.setData(time, array.flatten())

    @QtCore.Slot(object, object, object, object)
    def fft_update_cb(self, channel_id: int, subchannel_id: int,
                      fft_freqs: NDArray[numpy.float64],
                      fft_data: Union[NDArray[numpy.float64], float]) -> None:
        selected_channel_id = self.get_current_channel_id()
        if channel_id != selected_channel_id:
            # old data
            return

        selected_subchannel_index = self.fftSubchannelComboBox.currentIndex()
        if subchannel_id != selected_subchannel_index:
            # old data
            return

        try:
            unit_formatter = self.channel_unit[channel_id].unit_formatter
        except KeyError:
            # disconnect in progress
            return

        if numpy.ndim(fft_data) == 0:
            # buffering
            if not self.buffering:
                self.bufferingLabel.setVisible(True)
                self.buffering = True

            try:
                percent = int(100 * fft_data)
                text = f"Buffering {percent}%"
            except Exception:
                text = "Buffering"
            self.bufferingLabel.setText(text)
        else:
            if self.buffering:
                self.bufferingLabel.setVisible(False)
                self.buffering = False
            # update the data using the unit formatter scale only. The offset
            # would apply to the DC value, but the fft input is mean subtracted
            fft_data *= unit_formatter.conversion_scale
            self.fft_curve.setData(fft_freqs, fft_data)

    def get_plot_pens(self, subchannel_count: int) -> list[str]:
        if subchannel_count == 1:
            return ['c']

        pens = ['b', 'g', 'r']
        if subchannel_count <= 3:
            return pens[:subchannel_count]

        return pens + ['c'] * (subchannel_count - len(pens))

    def save_plot_range(self, channel_id: int) -> None:
        save_dict = self.saved_plot_ranges.setdefault(channel_id, {})

        time_vb = self.timePlot.getViewBox()
        if not isinstance(time_vb, pyqtgraph.ViewBox):
            return

        time_autorange = time_vb.autoRangeEnabled()
        time_range = time_vb.targetRange()
        save_dict['time'] = (time_autorange, time_range)

        if self.fft_curve.getData()[0] is not None:
            fft_vb: pyqtgraph.ViewBox = \
                self.fftPlot.getViewBox()  # type: ignore

            if not isinstance(fft_vb, pyqtgraph.ViewBox):
                return

            fft_autorange = fft_vb.autoRangeEnabled()
            fft_range = fft_vb.targetRange()
            save_dict['fft'] = (fft_autorange, fft_range)

    def restore_plot_range(self, channel_id: int) -> None:
        save_dict = self.saved_plot_ranges.get(channel_id, {})

        def restore(vb: pyqtgraph.ViewBox, autorange: tuple[bool, bool],
                    targetrange: list) -> None:
            x_autorange, y_autorange = autorange

            # restore the autorange
            vb.enableAutoRange(x=x_autorange, y=y_autorange)

            if not x_autorange:
                vb.setXRange(*targetrange[0], update=False, padding=0.0)
            if not y_autorange:
                vb.setYRange(*targetrange[1], update=False, padding=0.0)

        if 'time' in save_dict:
            restore(cast(pyqtgraph.ViewBox, self.timePlot.getViewBox()),
                    *save_dict['time'])
        else:
            restore(cast(pyqtgraph.ViewBox, self.timePlot.getViewBox()),
                    (True, True), [])

        if 'fft' in save_dict:
            restore(cast(pyqtgraph.ViewBox, self.fftPlot.getViewBox()),
                    *save_dict['fft'])
        else:
            restore(cast(pyqtgraph.ViewBox, self.fftPlot.getViewBox()),
                    (True, True), [])

    @QtCore.Slot()
    def graph_channel_changed(self) -> None:
        self.fftSubchannelComboBox.clear()
        self.timePlot.clear()
        self.time_curves.clear()
        self.fft_curve.clear()

        channel_id = self.get_current_channel_id()
        if channel_id is None:
            return

        if self.last_plot_range_channel_id is not None:
            self.save_plot_range(self.last_plot_range_channel_id)

        channel_info = self.controller.channel_info[channel_id]

        for subchannel_name in channel_info.subchannel_names:
            self.fftSubchannelComboBox.addItem(subchannel_name)

        subchannel_count = len(channel_info.subchannel_names)
        if subchannel_count > 1:
            self.fftSubchannelComboBox.setEnabled(True)
        else:
            self.fftSubchannelComboBox.setEnabled(False)

        # remove the legend
        if self.legend:
            self.legend.scene().removeItem(self.legend)
            self.timePlot.legend = None
            self.legend = None

        if subchannel_count > 1:
            self.legend = self.timePlot.addLegend()

        pens = self.get_plot_pens(subchannel_count)
        for pen, subchannel_name in zip(pens, channel_info.subchannel_names):
            curve = self.timePlot.plot(pen=pen, name=subchannel_name)
            curve.setZValue(1)
            self.time_curves.append(curve)

        unit_option = self.channel_unit[channel_id]

        time_axis = self.timePlot.getAxis('left')
        fft_axis = self.fftPlot.getAxis('left')
        if unit_option.metric_scale is not None:
            time_axis.setScale(unit_option.metric_scale)
            time_axis.setLabel("", units=unit_option.base_str)
            fft_axis.setScale(unit_option.metric_scale)
            fft_axis.setLabel("", units=unit_option.base_str)
        else:
            time_axis.setScale(1.0)
            time_axis.setLabel(unit_option.base_str, units="")
            fft_axis.setScale(1.0)
            fft_axis.setLabel(unit_option.base_str, units="")

        if self.preferences.plot_mean:
            plot_rate = channel_info.rate / channel_info.downsample_factor
            factor = math.ceil(plot_rate)
            if factor > 1:
                self.timePlot.setDownsampling(factor, False, "mean")
            else:
                self.timePlot.setDownsampling(False, False, "mean")
        else:
            # set to auto downsampling with peak for best performance on
            # large datasets
            self.timePlot.setDownsampling(None, True, "peak")

        # add region for FFT size
        if channel_info.fft_shortened:
            duration = channel_info.fft_sample_len / channel_info.rate
            lr = pyqtgraph.LinearRegionItem([-duration, 0], movable=False)
            self.timePlot.addItem(lr)

        self.restore_plot_range(channel_id)
        self.last_plot_range_channel_id = channel_id

    def _unit_selected(self, channel_id: int, unit_option: UnitOption) -> None:
        self.channel_unit[channel_id] = unit_option
        self.graph_channel_changed()

    @QtCore.Slot()
    def fft_subchannel_changed(self) -> None:
        self.fft_curve.clear()
        channel_id = self.get_current_channel_id()
        subchannel_index = self.fftSubchannelComboBox.currentIndex()
        self.controller.plot_change(channel_id, subchannel_index)

    def set_is_shown(self, is_shown: bool) -> None:
        self.controller.set_is_shown(is_shown)

    def create_rgb_widget(self, index: int,
                          initial_values: tuple[int, int, int],
                          manual_control: bool) -> None:
        set_values = functools.partial(self.controller.set_rgb, index)
        widget = RGBControlWidget(set_values, initial_values)
        widget.setEnabled(manual_control)
        self.LEDLayout.addWidget(widget)
        self.rgb_widgets.append(widget)

    def create_led_widget(self, index: int, initial_value: int,
                          manual_control: bool) -> None:
        set_value = functools.partial(self.controller.set_led, index)
        widget = LEDControlWidget(set_value, initial_value)
        widget.setEnabled(manual_control)
        self.LEDLayout.addWidget(widget)
        self.led_widgets.append(widget)

    def setup_rgb_and_led_widgets(self, device_info: DeviceInfo,
                                  manual_control: bool) -> None:
        # clear old widgets
        while True:
            item = self.LEDLayout.takeAt(0)
            if not item:
                break

        for rgb_widget in self.rgb_widgets:
            rgb_widget.deleteLater()
        self.rgb_widgets.clear()

        for led_widget in self.led_widgets:
            led_widget.deleteLater()
        self.led_widgets.clear()

        # create widgets
        for i, values in enumerate(device_info.rgb_settings):
            self.create_rgb_widget(i, values, manual_control)
        for i, value in enumerate(device_info.led_settings):
            self.create_led_widget(i, value, manual_control)

    def setup_ctrl_vars(self, device_info: DeviceInfo,
                        manual_control: bool) -> None:
        self.rf_power_panel.clear_ctrl_var_widgets()
        self.radio_panel.clear_ctrl_var_widgets()
        self.ctrl_var_panel.clear_ctrl_var_widgets()

        for ctrl_var in self.ctrl_var_widgets:
            ctrl_var.deleteLater()
        self.ctrl_var_widgets.clear()

        # create new ones
        ctrl_vars = device_info.ctrl_vars
        for index, (name, ctrl_var_info, setting) in enumerate(ctrl_vars):
            if setting is None:
                continue  # missing current value
            set_value = functools.partial(self.controller.set_ctrl_var, index)
            widget = CtrlVarWidget(
                set_value, name, ctrl_var_info, setting)
            widget.setEnabled(manual_control)
            self.ctrl_var_widgets.append(widget)

        unassigned_ctrl_var_indexes = set(range(len(ctrl_vars)))

        if device_info.rf_power_ctrl_vars:
            for index in device_info.rf_power_ctrl_vars:
                unassigned_ctrl_var_indexes.discard(index)
                widget = self.ctrl_var_widgets[index]
                self.rf_power_panel.add_ctrl_var_widget(widget)

        if device_info.radio_ctrl_vars:
            for index in device_info.radio_ctrl_vars:
                unassigned_ctrl_var_indexes.discard(index)
                widget = self.ctrl_var_widgets[index]
                self.radio_panel.add_ctrl_var_widget(widget)

        for index in sorted(unassigned_ctrl_var_indexes):
            self.ctrl_var_panel.add_ctrl_var_widget(
                self.ctrl_var_widgets[index])
        self.ctrl_var_panel.setVisible(bool(unassigned_ctrl_var_indexes))

    def setup_channel(self, channel_id: int,
                      channel_info: ChannelInformation) -> None:
        channel = channel_info.channel

        unit_options = get_unit_options(channel.unit_type, channel.minimum,
                                        channel.maximum, channel.resolution)
        default = get_default_option(
            self.settings, channel.unit_type, unit_options)

        action_group = QtGui.QActionGroup(self)
        unit_actions: list[QtGui.QAction] = []
        for unit_option in unit_options:
            action = QtGui.QAction(action_group)
            if unit_option.metric_relation:
                action.setText("{} ({})".format(
                    unit_option.base_str, unit_option.metric_relation))
            else:
                action.setText(unit_option.base_str)
            action.setCheckable(True)
            if unit_option == default:
                action.setChecked(True)
            action_cb = functools.partial(
                self._unit_selected, channel_id, unit_option)
            action.triggered.connect(action_cb)

            unit_actions.append(action)

        self.channel_unit_options[channel_id] = unit_options
        self.channel_unit_actions[channel_id] = unit_actions
        self.channel_unit_action_group[channel_id] = action_group
        self.channel_unit_type[channel_id] = channel.unit_type
        self.channel_unit_default[channel_id] = default
        self.channel_unit[channel_id] = default

        field_list = []
        alert_actions: list[QtGui.QAction] = []

        for i, subchannel_name in enumerate(channel_info.subchannel_names):
            label = QtWidgets.QLabel(subchannel_name)

            mean_field = MeasurementLineEdit(unit_actions)
            std_dev_field = MeasurementLineEdit(unit_actions)
            sampling_rate_field = MeasurementLineEdit(None)

            sampling_rate = "{:g} sps".format(channel_info.rate)
            sampling_rate_field.setText(sampling_rate)

            edit_alert_button = QtWidgets.QToolButton()
            edit_alert_action = EditAlertAction(
                channel_id, i, subchannel_name, self, edit_alert_button)
            edit_alert_button.setDefaultAction(edit_alert_action)
            alert_actions.append(edit_alert_action)

            row = self.channelLayout.rowCount()
            self.channelLayout.addWidget(label, row, 0)
            self.channelLayout.addWidget(mean_field, row, 1)
            self.channelLayout.addWidget(std_dev_field, row, 2)
            self.channelLayout.addWidget(sampling_rate_field, row, 3)
            self.channelLayout.addWidget(edit_alert_button, row, 4)
            field_list.append((mean_field, std_dev_field))

        self.subchannel_fields[channel_id] = field_list
        self.channel_alert_actions[channel_id] = alert_actions

    def disable_interaction(self) -> None:
        self.actionCalibrate.setEnabled(False)
        self.actionChangeActiveStreams.setEnabled(False)
        self.actionEditDeviceSettings.setEnabled(False)
        self.actionFirmwareFromBranch.setEnabled(False)
        self.actionFirmwareFromCommit.setEnabled(False)
        self.actionFirmwareFromFile.setEnabled(False)
        self.actionFirmwareLatestStable.setEnabled(False)
        self.actionForceReset.setEnabled(False)
        self.actionForceRunApplication.setEnabled(False)
        self.actionForceRunBootloader.setEnabled(False)
        self.actionRaiseException.setEnabled(False)
        self.actionRecoverNVM.setEnabled(False)
        self.actionRFTest.setEnabled(False)
        self.actionRunTests.setEnabled(False)
        self.actionSetDeviceMode.setEnabled(False)
        self.actionSetUserTag1.setEnabled(False)
        self.actionSetUserTag2.setEnabled(False)
        self.actionShakerCalibrate.setEnabled(False)
        if self.calibration_panel:
            self.calibration_panel.setEnabled(False)
        self.firmware_menu.setEnabled(False)
        self.menuButton.setEnabled(False)
        self.radio_panel.setEnabled(False)

    def device_info_updated(self, device_info: DeviceInfo,
                            manual_control: bool) -> None:
        old_channel_id = self.get_current_channel_id()
        new_index = None

        self.last_channel_id = None
        self.combo_box_channel_ids.clear()
        self.graphChannelComboBox.clear()
        self.subchannel_fields.clear()
        self.channel_unit_options.clear()
        self.channel_unit_actions.clear()
        for action_group in self.channel_unit_action_group.values():
            action_group.deleteLater()
        self.channel_unit_action_group.clear()
        self.channel_unit_type.clear()
        self.channel_unit_default.clear()
        self.channel_unit.clear()

        if device_info.user_tag_1 is None:
            self.userTag1.setText(self.tr("<INVALID>"))
        elif not device_info.user_tag_1:
            self.userTag1.setText(self.tr("<EMPTY>"))
        else:
            self.userTag1.setText(device_info.user_tag_1)

        self.plotmain.update_device_name(self, self.controller.display_name)

        self.tree_item.setText(1, device_info.user_tag_1 or "")
        self.tree_item.setText(2, device_info.user_tag_2 or "")
        self.tree_item.setText(3, "{} rev {}".format(*device_info.board_info))
        self.tree_item.setText(4, device_info.build_info)
        self.tree_item.setText(5, device_info.build_date)

        if device_info.user_tag_2 is None:
            self.userTag2.setText(self.tr("<INVALID>"))
        elif not device_info.user_tag_2:
            self.userTag2.setText(self.tr("<EMPTY>"))
        else:
            self.userTag2.setText(device_info.user_tag_2)

        self.boardInfo.setText("{} rev {}".format(*device_info.board_info))
        self.buildInfo.setText(device_info.build_info)
        self.buildDate.setText(device_info.build_date)

        if device_info.repo_branch:
            self.branch.setText(device_info.repo_branch)
            self.branch.setVisible(True)
            self.branchLabel.setVisible(True)
        else:
            self.branch.setText("")
            self.branch.setVisible(False)
            self.branchLabel.setVisible(False)

        self.update_supply_display(device_info)

        if device_info.supports_bootloader:
            self.bootloaderIndicator.setVisible(True)
        else:
            self.bootloaderIndicator.setVisible(False)

        if device_info.nvm_modified:
            self.nvmModifiedIndicator.setVisible(True)
        else:
            self.nvmModifiedIndicator.setVisible(False)

        if len(device_info.settings) == 0:
            # No settings on the device
            self.actionEditDeviceSettings.setEnabled(False)
            self.actionEditDeviceSettings.setText(
                self.tr("No Device Settings"))
        else:
            self.actionEditDeviceSettings.setEnabled(manual_control)
            self.actionEditDeviceSettings.setText(
                self.tr("Edit Device Settings"))

        self.advanced_menu.setEnabled(manual_control)
        self.actionForceRunApplication.setEnabled(
            device_info.supports_bootloader and manual_control)
        can_run_bootloader = device_info.bootloader_info == "Asphodel"
        self.actionForceRunBootloader.setEnabled(
            can_run_bootloader and manual_control)
        self.actionForceReset.setEnabled(manual_control)
        self.actionRaiseException.setEnabled(manual_control)
        self.actionRecoverNVM.setEnabled(manual_control)

        bootloader_available = (device_info.supports_bootloader
                                or can_run_bootloader)
        self.firmware_menu.setEnabled(bootloader_available and manual_control)
        self.actionFirmwareLatestStable.setEnabled(
            bootloader_available and manual_control)
        self.actionFirmwareFromBranch.setEnabled(
            bootloader_available and manual_control)
        self.actionFirmwareFromCommit.setEnabled(
            bootloader_available and manual_control)
        self.actionFirmwareFromFile.setEnabled(
            bootloader_available and manual_control)

        self.actionSetDeviceMode.setEnabled(
            device_info.supports_device_mode and manual_control)

        self.actionRFTest.setEnabled(
            (device_info.supports_radio or device_info.supports_remote)
            and manual_control)

        self.menu.setEnabled(True)
        self.actionChangeActiveStreams.setEnabled(manual_control)
        self.actionRunTests.setEnabled(manual_control)
        self.menuButton.setEnabled(True)

        self.actionSetUserTag1.setEnabled(manual_control)
        self.actionSetUserTag2.setEnabled(manual_control)

        self.setup_rgb_and_led_widgets(device_info, manual_control)

        self.setup_ctrl_vars(device_info, manual_control)

        # set panel visibility
        self.rf_power_panel.setVisible(device_info.supports_rf_power)
        self.radio_panel.setVisible(device_info.supports_radio)
        self.radio_panel.setEnabled(manual_control)
        self.remote_panel.setVisible(device_info.supports_remote)

        # clear the graphs
        self.graph_channel_changed()

        # reset the channel layout
        to_delete: list[QtWidgets.QWidget] = []
        for i in range(self.channelLayout.count()):
            position = self.channelLayout.getItemPosition(i)
            row, _col, _rs, _cs = position  # type: ignore
            if row != 0:
                to_delete.append(self.channelLayout.itemAt(i).widget())
        for widget in to_delete:
            self.channelLayout.removeWidget(widget)
            widget.deleteLater()

        self.channel_alert_actions.clear()

        sorted_channel_info = sorted(self.controller.channel_info.items())
        for channel_id, channel_info in sorted_channel_info:
            self.setup_channel(channel_id, channel_info)

            if channel_id == old_channel_id:
                new_index = len(self.combo_box_channel_ids)
            self.combo_box_channel_ids.append(channel_id)
            self.graphChannelComboBox.addItem(channel_info.name)

        self.update_alert_action_icons()

        if self.graphChannelComboBox.count() > 0:
            if new_index is None:
                self.graphChannelComboBox.setCurrentIndex(0)
            else:
                self.graphChannelComboBox.setCurrentIndex(new_index)
        else:
            self.graphChannelComboBox.setCurrentIndex(-1)

        self.create_calibration_info(device_info, manual_control)

    def get_current_channel_id(self) -> Optional[int]:
        index = self.graphChannelComboBox.currentIndex()
        if index == -1:
            return None
        try:
            return self.combo_box_channel_ids[index]
        except IndexError:
            return None

    @QtCore.Slot()
    def close_controller(self) -> None:
        self.logger.debug("Close button pressed")
        self.controller.clear_manual_control()
        self.plotmain.dispatcher.mark_manually_disconnected(self.controller)

    @QtCore.Slot(object, str)
    def controller_state_changed(self, state: DeviceControllerState,
                                 message: str) -> None:
        self.statusLabel.setText(message)
        if state == DeviceControllerState.DISCONNECTED:
            self.statusProgressBar.setVisible(False)
            self.stackedWidget.setCurrentIndex(0)
            self.plotmain.set_tab_disconnected(self)
            self.disable_interaction()
        elif state == DeviceControllerState.CONNECTING:
            # device info is being fetched: setup the progress bar
            self.stackedWidget.setCurrentIndex(0)
            self.plotmain.set_tab_disconnected(self)
            self.disable_interaction()
            self.statusProgressBar.setMinimum(0)
            self.statusProgressBar.setMaximum(0)
            self.statusProgressBar.setValue(0)
            self.statusProgressBar.setVisible(True)
        elif state == DeviceControllerState.STREAMING_STARTING:
            # device info is ready: set bar to 100%
            self.statusProgressBar.setValue(self.statusProgressBar.maximum())

            # NOTE: this if statement is redundant, but useful for type safety
            if self.controller.device_info:
                manual_control = self.controller.get_manual_control()
                self.device_info_updated(self.controller.device_info,
                                         manual_control)

            if not self.controller.active_streams:
                if self.buffering:
                    self.bufferingLabel.setVisible(False)
                    self.buffering = False
                self.noChannelsTimeLabel.setVisible(True)
                self.noChannelsFreqLabel.setVisible(True)
            else:
                self.noChannelsTimeLabel.setVisible(False)
                self.noChannelsFreqLabel.setVisible(False)

        elif state == DeviceControllerState.RUNNING:
            # streaming running
            self.stackedWidget.setCurrentIndex(1)
            self.plotmain.set_tab_connected(self)
            self.statusProgressBar.setVisible(False)
        elif state == DeviceControllerState.RUNNING_FUNCTION:
            # running a dedicated function
            pass

    @QtCore.Slot(int, int, str)
    def progress_update(self, finished: int, total: int, message: str) -> None:
        self.statusProgressBar.setMaximum(total)
        self.statusProgressBar.setValue(finished)
        self.statusProgressBar.setVisible(True)
        self.statusLabel.setText(message)

    @QtCore.Slot(int, object)
    def rgb_updated_cb(self, index: int, values: tuple[int, int, int]) -> None:
        try:
            widget = self.rgb_widgets[index]
        except IndexError:
            return
        widget.set_values(values)

    @QtCore.Slot(int, int)
    def led_updated_cb(self, index: int, value: int) -> None:
        try:
            widget = self.led_widgets[index]
        except IndexError:
            return
        widget.set_value(value)

    @QtCore.Slot(int, int)
    def ctrl_var_updated_cb(self, index: int, value: int) -> None:
        try:
            widget = self.ctrl_var_widgets[index]
        except IndexError:
            return
        widget.set_value(value)

    @QtCore.Slot(int, int)
    def download_update_progress(self, read_bytes: int,
                                 total_length: int) -> None:
        self.firmware_progress.setMaximum(total_length)
        self.firmware_progress.setMinimum(read_bytes)

    @QtCore.Slot(object, str)
    def download_error(self, file: io.BytesIO, error_str: str) -> None:
        self.firmware_progress.reset()
        file.close()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)

    @QtCore.Slot(str, object)
    def download_completed(self, url: str, file: io.BytesIO) -> None:
        self.firmware_progress.reset()

        firmware_bytes = file.getvalue()

        try:
            firm_data = bootloader.decode_firm_bytes(firmware_bytes)
        except Exception:
            self.logger.exception('Error decoding downloaded firmware')
            m = self.tr('Error decoding downloaded firmware!')
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), m)
            return
        finally:
            file.close()

        self.firmware_cache.set(url, firmware_bytes)

        self.controller.load_firmware(firm_data, url)

    @QtCore.Slot(str)
    def firmware_finder_error(self, error_str: str) -> None:
        self.firmware_progress.reset()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)

    @QtCore.Slot(object)
    def firmware_finder_completed(self, build_urls: dict[str, str]) -> None:
        self.firmware_progress.reset()
        build_types = sorted(build_urls.keys())
        if 'firmware' in build_types:
            # move it to the front
            build_types.remove('firmware')
            build_types.insert(0, 'firmware')

        if len(build_types) == 1:
            # choose the only option available
            build_type = build_types[0]
        else:
            value, ok = QtWidgets.QInputDialog.getItem(
                self, self.tr("Select Build Type"),
                self.tr("Select Build Type"), build_types, 0,
                editable=False)
            if not ok:
                return
            build_type = value

        url: str = build_urls[build_type]

        firmware_bytes = cast(Optional[bytes],
                              self.firmware_cache.get(url, None))
        if firmware_bytes:
            self.logger.info("Using cached firmware from %s", url)

            try:
                firm_data = bootloader.decode_firm_bytes(firmware_bytes)
            except Exception:
                self.logger.exception(
                    'Error decoding cached firmware. Removing from cache.')
                self.firmware_cache.delete(url)
                firm_data = None

            if firm_data:
                self.controller.load_firmware(firm_data, url)
                return

        self.logger.info("Downloading firmware from %s", url)

        self.firmware_progress.setMinimum(0)
        self.firmware_progress.setMaximum(0)
        self.firmware_progress.setValue(0)
        self.firmware_progress.setLabelText(
            self.tr("Downloading firmware..."))
        self.firmware_progress.forceShow()

        file = io.BytesIO()
        self.downloader.start_download(url, file)

    def do_bootloader_web(self, build_type: Optional[str],
                          branch: Optional[str] = None,
                          commit: Optional[str] = None) -> None:
        if self.controller.device_info is None:
            return

        self.firmware_progress.setMinimum(0)
        self.firmware_progress.setMaximum(0)
        self.firmware_progress.setValue(0)
        self.firmware_progress.setLabelText(
            self.tr("Searching for firmware..."))
        self.firmware_progress.forceShow()

        repo = self.controller.device_info.repo_name
        if not repo:
            board_info = self.controller.device_info.board_info
        else:
            board_info = None

        self.firmware_finder.find_firmware(
            build_type, board_info, repo=repo, branch=branch, commit=commit)

    @QtCore.Slot()
    def do_bootloader_latest_stable(self) -> None:
        self.do_bootloader_web(build_type="firmware", branch="master")

    @QtCore.Slot(object)
    def ref_finder_completed(self, refs: list[dict[str, Any]]) -> None:
        self.firmware_progress.reset()

        if self.controller.device_info is None:
            return

        default_branch = self.controller.device_info.repo_branch
        if not default_branch:
            default_branch = "master"

        branch_choices = [default_branch]
        if default_branch != "master":
            branch_choices.append("master")
        if default_branch != "develop":
            branch_choices.append("develop")

        ref_names = []
        for ref in refs:
            ref_name = ref.get("name", None)
            if ref_name and ref_name not in branch_choices:
                ref_names.append(ref_name)

        if refs:
            label = self.tr("Firmware Branch:")
        else:
            label = self.tr("No branches found!\nFirmware Branch:")

        branch_choices.extend(sorted(ref_names,
                                     key=hyperborea.download.ref_sort_key))

        branch, ok = QtWidgets.QInputDialog.getItem(
            self, self.tr("Firmware Branch"), label, branch_choices, 0, True)
        if not ok:
            return

        branch = branch.strip()

        self.do_bootloader_web(build_type=None, branch=branch)

    @QtCore.Slot()
    def ref_finder_error(self) -> None:
        self.ref_finder_completed([])

    @QtCore.Slot()
    def do_bootloader_from_branch(self) -> None:
        if self.controller.device_info is None:
            return

        self.firmware_progress.setMinimum(0)
        self.firmware_progress.setMaximum(0)
        self.firmware_progress.setValue(0)
        self.firmware_progress.setLabelText(
            self.tr("Collecting branches..."))
        self.firmware_progress.forceShow()

        repo = self.controller.device_info.repo_name
        if not repo:
            board_info = self.controller.device_info.board_info
        else:
            board_info = None

        self.ref_finder.get_firmware_refs(board_info=board_info, repo=repo)

    @QtCore.Slot()
    def do_bootloader_from_commit(self) -> None:
        commit, ok = QtWidgets.QInputDialog.getText(
            self, self.tr("Firmware Commit"), self.tr("Firmware Commit:"),
            QtWidgets.QLineEdit.EchoMode.Normal, "")
        if not ok:
            return

        commit = commit.strip()

        self.do_bootloader_web(build_type=None, commit=commit)

    def get_firmware_file(self, device_info: DeviceInfo) -> Optional[str]:
        settings = QtCore.QSettings()

        board_name, board_rev = device_info.board_info
        short_board_name = board_name.replace(" ", "")

        keys = [f"firmDirectory/{short_board_name}/Rev{board_rev}",
                f"firmDirectory/{short_board_name}/last",
                "firmDirectory/last"]

        # find the directory from settings
        firm_dir = None
        for key in keys:
            test_dir = settings.value(key)
            if test_dir and isinstance(test_dir, str):
                if os.path.isdir(test_dir):
                    firm_dir = test_dir
                    break
        if not firm_dir:
            firm_dir = ""

        # ask the user for the file name
        caption = self.tr("Open Firmware File")
        file_filter = self.tr("Firmware Files (*.firmware);;All Files (*.*)")
        val = QtWidgets.QFileDialog.getOpenFileName(self, caption, firm_dir,
                                                    file_filter)
        output_path = val[0]

        if output_path:
            # save the directory
            output_dir = os.path.dirname(output_path)
            for key in keys:
                settings.setValue(key, output_dir)
            return output_path
        else:
            return None

    @QtCore.Slot()
    def do_bootloader_from_file(self) -> None:
        if self.controller.device_info is None:
            return

        base_dir = self.preferences.firmware_root_dir
        if base_dir:
            base_dir = str(base_dir)  # make sure it's a string
        firm_dir, firm_name = bootloader.get_default_file(
            self.controller.device_info, base_dir)

        if not firm_dir:
            firm_file = self.get_firmware_file(self.controller.device_info)
        else:
            firm_file = os.path.join(firm_dir, firm_name)

            message = self.tr("Use {}?").format(firm_file)
            ret = QtWidgets.QMessageBox.question(
                self, self.tr("Update Firmware"), message,
                QtWidgets.QMessageBox.StandardButton.Yes |
                QtWidgets.QMessageBox.StandardButton.No |
                QtWidgets.QMessageBox.StandardButton.Cancel,
                QtWidgets.QMessageBox.StandardButton.Yes)
            if ret == QtWidgets.QMessageBox.StandardButton.Cancel:
                return
            if ret == QtWidgets.QMessageBox.StandardButton.No:
                firm_file = self.get_firmware_file(self.controller.device_info)

        if not firm_file:
            return  # user cancelled

        try:
            firm_data = bootloader.decode_firm_file(firm_file)
        except Exception:
            self.logger.exception('Error loading firmware from "%s"',
                                  firm_file)
            m = self.tr('Error loading firmware from file!')
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), m)
            return

        url = pathlib.Path(firm_file).resolve().as_uri()
        self.controller.load_firmware(firm_data, url)

    @QtCore.Slot(object)
    def alerts_changed_cb(self, alerts: frozenset[str]) -> None:
        for channel_id, fields in self.subchannel_fields.items():
            for i, (mean_field, std_dev_field) in enumerate(fields):
                for limit_type in (LimitType.MEAN_HIGH_LIMIT,
                                   LimitType.MEAN_LOW_LIMIT):
                    id = f'_alert_{channel_id}_{i}_{limit_type}'
                    if id in alerts:
                        mean_field.set_alert(True)
                        break
                else:
                    mean_field.set_alert(False)

                for limit_type in (LimitType.STD_HIGH_LIMIT,
                                   LimitType.STD_LOW_LIMIT):
                    id = f'_alert_{channel_id}_{i}_{limit_type}'
                    if id in alerts:
                        std_dev_field.set_alert(True)
                        break
                else:
                    std_dev_field.set_alert(False)

    def update_alert_action_icons(self) -> None:
        for channel_id, alert_actions in self.channel_alert_actions.items():
            for i, alert_action in enumerate(alert_actions):
                alert_limits = self.controller.device_prefs.get_alert_limits(
                    channel_id, i)
                if alert_limits:
                    alert_action.setIcon(
                        QtGui.QIcon.fromTheme("signal_flag_red"))
                else:
                    alert_action.setIcon(
                        QtGui.QIcon.fromTheme("signal_flag_white"))

    @QtCore.Slot(bool)
    def _manual_control_changed_cb(self, manual_control: bool) -> None:
        if self.controller.device_info:
            self.device_info_updated(self.controller.device_info,
                                     manual_control)
        self.closeButton.setEnabled(manual_control)

    @QtCore.Slot()
    def schedule_or_trigger_count_updated(self) -> None:
        trigger_count = self.controller.trigger_count
        schedule_count = self.controller.schedule_count

        if trigger_count == 1:
            trigger_str = self.tr("1 trigger")
        elif trigger_count > 1:
            trigger_str = self.tr("{} triggers").format(trigger_count)
        else:
            trigger_str = ""

        if schedule_count == 1:
            schedule_str = self.tr("1 schedule item")
        elif schedule_count > 1:
            schedule_str = self.tr("{} schedule items").format(
                schedule_count)
        else:
            schedule_str = ""

        self.tree_item.setText(6, str(schedule_count))

        if trigger_str and schedule_str:
            self.scheduleLabel.setText(trigger_str + ", " + schedule_str)
            self.scheduleLabel.setVisible(True)
        elif trigger_str:
            self.scheduleLabel.setText(trigger_str)
            self.scheduleLabel.setVisible(True)
        elif schedule_str:
            self.scheduleLabel.setText(schedule_str)
            self.scheduleLabel.setVisible(True)
        else:
            self.scheduleLabel.setText("")
            self.scheduleLabel.setVisible(False)

    @QtCore.Slot(object, object, object)
    def active_triggers_changed_cb(self, controller: DeviceController,
                                   active_triggers: frozenset[str],
                                   inactive_triggers: frozenset[str]) -> None:
        active_str = ", ".join(sorted(active_triggers, key=str.casefold))
        self.tree_item.setText(7, active_str)
        inactive_str = ", ".join(sorted(inactive_triggers, key=str.casefold))
        self.tree_item.setText(8, inactive_str)

    @QtCore.Slot()
    def show_remote_tab(self) -> None:
        remote_controller = self.controller.remote_controller
        if remote_controller:
            remote_tab = self.plotmain.get_tab_widget(
                remote_controller)
            if remote_tab:
                self.plotmain.show_tab(remote_tab, self)

    @QtCore.Slot()
    def show_radio_tab(self) -> None:
        radio_controller = self.controller.parent_controller
        if radio_controller:
            radio_tab = self.plotmain.get_tab_widget(
                radio_controller)
            if radio_tab:
                self.plotmain.show_tab(radio_tab, self)
