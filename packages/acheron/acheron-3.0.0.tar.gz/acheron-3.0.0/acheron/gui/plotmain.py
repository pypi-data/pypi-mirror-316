import bisect
import datetime
import logging
import math
import os
import subprocess
import sys
import tempfile
from typing import Any, BinaryIO, Optional, Union
import urllib.parse

import diskcache
from PySide6 import QtCore, QtGui, QtSvgWidgets, QtWidgets

import asphodel
from hyperborea.dark_mode import set_style
import hyperborea.download

from .. import build_info
from ..core.dispatcher import Dispatcher
from ..core.device_controller import DeviceController
from ..core.preferences import Preferences
from ..connectivity.s3upload import S3UploadManager
from ..disk.schedule_reader import ScheduleReader
from .about import AboutDialog
from .device_tab import DeviceTab
from .tcp_connect_dialog import TCPConnectDialog
from .download_firmware_dialog import DownloadFirmwareDialog
from .preferences_dialog import PreferencesDialog
from .tcp_scan_dialog import TCPScanDialog
from .ui.ui_plotmain import Ui_PlotMainWindow

logger = logging.getLogger(__name__)


class PaddedItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, padding: int = 10, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.padding = padding

    def sizeHint(self, option: QtWidgets.QStyleOptionViewItem,
                 index: Union[QtCore.QModelIndex,
                              QtCore.QPersistentModelIndex]) -> QtCore.QSize:
        size = super().sizeHint(option, index)
        size.setWidth(size.width() + self.padding)
        return size

    def paint(self, painter: QtGui.QPainter,
              option: QtWidgets.QStyleOptionViewItem,
              index: Union[QtCore.QModelIndex,
                           QtCore.QPersistentModelIndex]) -> None:
        option.rect.setWidth(  # type: ignore
            option.rect.width() - self.padding)  # type: ignore
        super().paint(painter, option, index)


class PlotMainWindow(Ui_PlotMainWindow, QtWidgets.QMainWindow):

    def __init__(self, dispatcher: Dispatcher, preferences: Preferences,
                 schedule_reader: ScheduleReader,
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.dispatcher = dispatcher
        self.preferences = preferences
        self.settings = QtCore.QSettings()  # things not worth putting in prefs
        self.schedule_reader = schedule_reader

        self.firmware_cache = diskcache.Cache(
            self.preferences.firmware_dir, size_limit=100e6)

        set_style(QtWidgets.QApplication.instance(),  # type: ignore
                  self.preferences.dark_mode)

        self.tab_widgets: list[DeviceTab] = []  # in display order
        self.tab_tree_items: dict[DeviceTab, QtWidgets.QTreeWidgetItem] = {}
        self.shown_tab: Optional[DeviceTab] = None

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup()
        self.setup_logo()

        self.setup_callbacks()
        self.setup_update_actions()

        self.collapsed = self.preferences.collapsed

        self.connecting_icon = QtGui.QIcon.fromTheme("nav_refresh_red")
        self.connected_icon = QtGui.QIcon.fromTheme("nav_plain_blue")

        if sys.platform == "darwin":
            # I couldn't figure out how to make menu work natively
            self.menubar.setNativeMenuBar(False)

        # restore window geometry
        geometry = self.settings.value('Geometry', b'')
        self.restoreGeometry(geometry)  # type: ignore

    def setup_logo(self) -> None:
        self.stackedWidget.setCurrentIndex(1)
        self.logo = QtSvgWidgets.QSvgWidget(":/logo.svg")
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored,
            QtWidgets.QSizePolicy.Policy.Ignored)
        self.logo.setSizePolicy(size_policy)

        def resizeEvent(event: QtGui.QResizeEvent) -> None:
            size = event.size()
            margins = self.logoLayout.contentsMargins()

            if size.width() == size.height():
                return

            full_width = size.width() + margins.left() + margins.right()
            full_height = size.height() + margins.top() + margins.bottom()

            d = min(full_width, full_height)
            top = math.ceil((full_height - d) / 2)
            bottom = math.floor((full_height - d) / 2)
            left = math.ceil((full_width - d) / 2)
            right = math.floor((full_width - d) / 2)
            self.logoLayout.setContentsMargins(left, top, right, bottom)

        self.logo.resizeEvent = resizeEvent  # type: ignore
        self.logoLayout.addWidget(self.logo)

        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.logo)
        self.opacity_effect.setOpacity(0.0)
        self.logo.setGraphicsEffect(self.opacity_effect)

        self.logo_animation = QtCore.QVariantAnimation(self)
        self.logo_animation.setStartValue(0.0)
        self.logo_animation.setEndValue(1.0)
        self.logo_animation.setDuration(1000)
        self.logo_animation.setEasingCurve(QtCore.QEasingCurve.Type.InQuart)
        self.logo_animation.valueChanged.connect(
            self.opacity_effect.setOpacity)
        self.logo_animation.start()

    def extra_ui_setup(self) -> None:
        app_name = QtWidgets.QApplication.applicationName()
        version = QtWidgets.QApplication.applicationVersion()
        is_frozen = getattr(sys, 'frozen', False)
        if is_frozen:
            title = self.tr("{} ({})").format(app_name, version)
        else:
            title = self.tr("{} (dev)").format(app_name)
        self.setWindowTitle(title)

        self.warningLabel.setVisible(False)

        self.rf_power_changed_cb(*self.dispatcher.get_rf_power_status())

        self.spacer = QtWidgets.QWidget()
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred)
        self.spacer.setSizePolicy(size_policy)
        self.toolBar.insertWidget(self.actionRescanUSB, self.spacer)

        if not asphodel.nativelib.usb_devices_supported:
            self.actionRescanUSB.setEnabled(False)
        if not asphodel.nativelib.tcp_devices_supported:
            self.actionFindTCPDevices.setEnabled(False)
            self.actionConnectTCPDevice.setEnabled(False)

        self.update_datetime_label()

        # hide the active triggers label
        self.active_triggers_changed(frozenset())

        if self.preferences.closeable_tabs:
            self.actionClosableTabs.setChecked(True)
            self.tabWidget.setTabsClosable(True)

        # remove the close buttons from the device tab
        tab_bar = self.tabWidget.tabBar()
        tab_bar.setTabButton(0, QtWidgets.QTabBar.ButtonPosition.LeftSide,
                             None)  # type: ignore
        tab_bar.setTabButton(0, QtWidgets.QTabBar.ButtonPosition.RightSide,
                             None)  # type: ignore

        # set the device tab icon
        self.tabWidget.setTabIcon(0, QtGui.QIcon.fromTheme("tree"))

        tree_header = self.treeWidget.header()
        tree_header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.treeWidget.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setItemDelegate(PaddedItemDelegate(16))

        self.update_progress = QtWidgets.QProgressDialog("", "", 0, 100)
        self.update_progress.setLabelText(self.tr(""))
        self.update_progress.setWindowTitle(self.tr("Check for Update"))
        self.update_progress.setCancelButton(None)  # type: ignore
        self.update_progress.setWindowModality(
            QtCore.Qt.WindowModality.WindowModal)
        self.update_progress.setMinimumDuration(0)
        self.update_progress.setAutoReset(False)
        self.update_progress.reset()

        self.actionAbout.setIcon(QtGui.QIcon.fromTheme("about"))
        self.actionConnectTCPDevice.setIcon(
            QtGui.QIcon.fromTheme("earth_network"))
        self.actionDisableRFPower.setIcon(
            QtGui.QIcon.fromTheme("antenna_stop"))
        self.actionDownloadFirmware.setIcon(QtGui.QIcon.fromTheme("install"))
        self.actionExit.setIcon(QtGui.QIcon.fromTheme("exit"))
        self.actionEnableRFPower.setIcon(QtGui.QIcon.fromTheme("antenna_play"))
        self.actionFindTCPDevices.setIcon(QtGui.QIcon.fromTheme("plug_lan"))
        self.actionMarkDirectory.setIcon(QtGui.QIcon.fromTheme("folder_up"))
        self.actionMarkFiles.setIcon(QtGui.QIcon.fromTheme("document_up"))
        self.actionPreferences.setIcon(QtGui.QIcon.fromTheme("preferences"))
        self.actionRescanUSB.setIcon(QtGui.QIcon.fromTheme("plug_usb"))
        self.actionUpdateCurrentBranch.setIcon(
            QtGui.QIcon.fromTheme("branch_element_new"))
        self.actionUpdateLatestStable.setIcon(QtGui.QIcon.fromTheme("branch"))
        self.actionUpdateSpecificBranch.setIcon(
            QtGui.QIcon.fromTheme("branch_view"))
        self.actionUpdateSpecificCommit.setIcon(
            QtGui.QIcon.fromTheme("symbol_hash"))
        self.menuCheckForUpdates.setIcon(
            QtGui.QIcon.fromTheme("cloud_computing_download"))

        self.upload_manager_changed_cb(self.dispatcher.upload_manager)

    def setup_callbacks(self) -> None:
        self.dispatcher.controller_created.connect(self.controller_created)
        self.dispatcher.controller_stopped.connect(self.remove_controller)
        self.dispatcher.initial_devices_connected.connect(
            self.initial_devices_connected_cb)

        self.actionEnableRFPower.triggered.connect(
            self.dispatcher.enable_all_rf_power)
        self.actionDisableRFPower.triggered.connect(
            self.dispatcher.disable_all_rf_power)
        self.dispatcher.rf_power_changed.connect(self.rf_power_changed_cb)

        self.dispatcher.upload_manager_changed.connect(
            self.upload_manager_changed_cb)

        self.dispatcher.active_triggers_changed.connect(
            self.active_triggers_changed)

        self.actionRescanUSB.triggered.connect(self.dispatcher.rescan_usb)
        self.actionFindTCPDevices.triggered.connect(self.find_tcp_devices)
        self.actionConnectTCPDevice.triggered.connect(self.connect_tcp_device)
        self.actionDisableStreaming.triggered.connect(
            self.set_disable_streaming)
        self.actionDisableArchiving.triggered.connect(
            self.set_disable_archiving)
        self.actionAbout.triggered.connect(self.show_about)
        self.actionChannelTable.triggered.connect(self.show_channel_table)
        self.actionPreferences.triggered.connect(self.show_preferences)
        self.actionReloadSchedule.triggered.connect(self.reload_schedule_cb)
        self.actionClosableTabs.triggered.connect(self.closable_tabs_cb)

        self.actionShowLogs.triggered.connect(self.show_log_dir)
        self.actionShowConfig.triggered.connect(self.show_config_dir)
        config = self.preferences.settings.fileName()
        if not os.path.exists(config):
            self.actionShowConfig.setVisible(False)

        self.clock_timer = QtCore.QTimer(self)
        self.clock_timer.timeout.connect(self.update_datetime_label)
        self.clock_timer.start(1000)  # 1 second intervals

        self.upload_timeout_timer = QtCore.QTimer(self)
        self.upload_timeout_timer.setSingleShot(True)
        self.upload_timeout_timer.timeout.connect(self.upload_timeout_cb)

        self.tabWidget.tabCloseRequested.connect(self.tab_close_requested)
        self.tabWidget.currentChanged.connect(self.current_tab_changed_cb)

        self.treeWidget.itemDoubleClicked.connect(
            self.tree_item_double_clicked)

        self.actionDownloadFirmware.triggered.connect(self.download_firmware)
        self.firmware_finder = hyperborea.download.FirmwareFinder(logger)
        self.firmware_finder.completed.connect(self.firmware_finder_completed)
        self.firmware_finder.error.connect(self.firmware_finder_error)
        self.firmware_downloader = hyperborea.download.Downloader(logger)
        self.firmware_downloader.update.connect(self.update_progress_cb)
        self.firmware_downloader.completed.connect(
            self.firmware_download_completed)
        self.firmware_downloader.error.connect(self.firmware_download_error)

        self.actionUpdateLatestStable.triggered.connect(
            self.update_latest_stable)
        self.actionUpdateCurrentBranch.triggered.connect(
            self.update_current_branch)
        self.actionUpdateSpecificBranch.triggered.connect(
            self.update_specific_branch)
        self.actionUpdateSpecificCommit.triggered.connect(
            self.update_specific_commit)

        self.software_finder = hyperborea.download.SoftwareFinder(logger)
        self.software_finder.completed.connect(self.update_finder_completed)
        self.software_finder.error.connect(self.update_finder_error)
        self.ref_finder = hyperborea.download.RefFinder(logger)
        self.ref_finder.completed.connect(self.ref_finder_completed)
        self.ref_finder.error.connect(self.ref_finder_error)
        self.software_downloader = hyperborea.download.Downloader(logger)
        self.software_downloader.update.connect(self.update_progress_cb)
        self.software_downloader.completed.connect(
            self.software_download_completed)
        self.software_downloader.error.connect(self.software_download_error)

        self.actionMarkDirectory.triggered.connect(self.mark_directory)
        self.actionMarkFiles.triggered.connect(self.mark_files)

        self.next_tab_shortcut = QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+PgDown"), self)
        self.next_tab_shortcut.activated.connect(self.next_tab)
        self.prev_tab_shortcut = QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+PgUp"), self)
        self.prev_tab_shortcut.activated.connect(self.prev_tab)

        self.schedule_reader.error.connect(self.schedule_error_cb)
        self.schedule_reader.warning.connect(self.schedule_warning_cb)

    def setup_update_actions(self) -> None:
        branch_name = build_info.get_branch_name()
        if not branch_name:
            self.menuCheckForUpdates.setEnabled(False)
            self.menuCheckForUpdates.setTitle(self.tr("Not Updatable"))
            self.actionUpdateLatestStable.setEnabled(False)
            self.actionUpdateCurrentBranch.setEnabled(False)
            self.actionUpdateSpecificBranch.setEnabled(False)
            self.actionUpdateSpecificCommit.setEnabled(False)
        elif branch_name == "master":
            # master is latest stable
            self.actionUpdateCurrentBranch.setEnabled(False)
            self.actionUpdateCurrentBranch.setVisible(False)
        else:
            action_str = self.tr("Latest {}").format(branch_name)
            self.actionUpdateCurrentBranch.setText(action_str)

    def find_update(self, branch: Optional[str] = None,
                    commit: Optional[str] = None,
                    fallback_branch: Optional[str] = None) -> None:
        build_key = build_info.get_build_key()
        if not build_key:
            return

        self.update_fallback_branch = fallback_branch

        self.update_progress.setMinimum(0)
        self.update_progress.setMaximum(0)
        self.update_progress.setValue(0)
        self.update_progress.setLabelText(self.tr("Checking for update..."))
        self.update_progress.forceShow()

        self.software_finder.find_software(
            "acheron", build_key, branch, commit)

    @QtCore.Slot(str)
    def update_finder_error(self, error_str: str) -> None:
        if self.update_fallback_branch:
            self.find_update(branch=self.update_fallback_branch)
        else:
            self.update_progress.reset()
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)

    @QtCore.Slot(object)
    def update_finder_completed(
            self, params: tuple[str, Optional[str], bool]) -> None:
        self.update_progress.reset()
        url, commit, ready = params

        if commit is not None and commit == build_info.get_commit_hash():
            logger.info("Up to date with commit %s", commit)
            QtWidgets.QMessageBox.information(
                self, self.tr("Up to date"),
                self.tr("Already running this version"))
            return

        if not ready:
            logger.info("Update is not ready")
            QtWidgets.QMessageBox.information(self,
                                              self.tr("Update not ready"),
                                              self.tr("Update is not ready"))
            return

        # ask if the user wants to proceed
        ret = QtWidgets.QMessageBox.question(
            self, self.tr("Update?"), self.tr("Update available. Update now?"),
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No)
        if ret != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        logger.info("Downloading update from %s", url)

        self.update_progress.setMinimum(0)
        self.update_progress.setMaximum(0)
        self.update_progress.setValue(0)
        self.update_progress.setLabelText(self.tr("Downloading update..."))
        self.update_progress.forceShow()

        fd, filename = tempfile.mkstemp(".exe", "setup-", text=False)
        file = os.fdopen(fd, "wb")
        file.filename = filename  # type: ignore
        self.software_downloader.start_download(url, file)

    @QtCore.Slot(int, int)
    def update_progress_cb(self, written_bytes: int,
                           total_length: int) -> None:
        if total_length != 0:
            self.update_progress.setMinimum(0)
            self.update_progress.setMaximum(total_length)
            self.update_progress.setValue(written_bytes)

    @QtCore.Slot(object, str)
    def software_download_error(self, file: BinaryIO, error_str: str) -> None:
        self.update_progress.reset()
        file.close()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)
        os.unlink(file.filename)  # type: ignore

    @QtCore.Slot(str, object)
    def software_download_completed(self, _url: str, file: BinaryIO) -> None:
        self.update_progress.reset()
        file.close()

        # stop the managers
        self.dispatcher.stop()

        # run the intstaller
        subprocess.Popen([
            file.filename,  # type: ignore
            '/silent', "/DeleteInstaller=Yes", "/SP-",
            "/SUPPRESSMSGBOXES", "/NORESTART", "/NOCANCEL"
        ])

        # close the application (though installer will force kill regardless)
        self.close()

    @QtCore.Slot()
    def update_latest_stable(self) -> None:
        self.find_update(branch="master")

    @QtCore.Slot()
    def update_current_branch(self) -> None:
        branch_name = build_info.get_branch_name()
        if not branch_name:
            return  # shouldn't be possible, but just in case

        if branch_name in ("master", "develop"):
            fallback = None
        else:
            fallback = "develop"

        self.find_update(branch=branch_name, fallback_branch=fallback)

    @QtCore.Slot()
    def update_specific_branch(self) -> None:
        self.update_progress.setMinimum(0)
        self.update_progress.setMaximum(0)
        self.update_progress.setValue(0)
        self.update_progress.setLabelText(self.tr("Collecting branches..."))
        self.update_progress.forceShow()

        self.ref_finder.get_software_refs("acheron")

    @QtCore.Slot()
    def ref_finder_error(self) -> None:
        self.ref_finder_completed([])

    @QtCore.Slot(object)
    def ref_finder_completed(self, refs: list[dict[str, Any]]) -> None:
        self.update_progress.reset()

        default_branch = build_info.get_branch_name()
        if default_branch is None:
            return  # shouldn't happen

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

        if ref_names:
            label = self.tr("Branch:")
        else:
            label = self.tr("No list of branches!\nBranch:")

        branch_choices.extend(sorted(ref_names,
                                     key=hyperborea.download.ref_sort_key))

        branch, ok = QtWidgets.QInputDialog.getItem(self, self.tr("Branch"),
                                                    label, branch_choices, 0,
                                                    True)
        if not ok:
            return

        branch = branch.strip()

        self.find_update(branch=branch)

    @QtCore.Slot()
    def update_specific_commit(self) -> None:
        commit, ok = QtWidgets.QInputDialog.getText(
            self, self.tr("Commit"), self.tr("Commit:"),
            QtWidgets.QLineEdit.EchoMode.Normal, "")
        if not ok:
            return

        commit = commit.strip()

        self.find_update(commit=commit)

    @QtCore.Slot()
    def download_firmware(self) -> None:
        dialog = DownloadFirmwareDialog(self)
        try:
            ret = dialog.exec()
            if ret == 0:
                return  # user cancelled

            results = dialog.get_results()
        finally:
            dialog.deleteLater()

        self.firmware_finder.find_firmware(build_type=None, **results)

    @QtCore.Slot(str)
    def firmware_finder_error(self, error_str: str) -> None:
        self.update_progress.reset()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)

    def get_firmware_save_file(self, default_name: str) -> Optional[str]:
        # find the directory from settings
        directory = self.settings.value("fileSaveDirectory")
        if directory:
            if isinstance(directory, str):
                if not os.path.isdir(directory):
                    directory = ""
            else:
                directory = ""
        else:
            directory = ""

        file_and_dir = os.path.join(directory, default_name)

        caption = self.tr("Save Firmware File")
        file_filter = self.tr("Firmware Files (*.firmware);;All Files (*.*)")
        val = QtWidgets.QFileDialog.getSaveFileName(self, caption,
                                                    file_and_dir, file_filter)
        output_path = val[0]

        if output_path:
            # save the directory
            output_dir = os.path.dirname(output_path)
            self.settings.setValue("fileSaveDirectory", output_dir)
            return output_path
        else:
            return None

    @QtCore.Slot(object)
    def firmware_finder_completed(self, build_urls: dict[str, Any]) -> None:
        self.update_progress.reset()
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
                self,
                self.tr("Select Build Type"),
                self.tr("Select Build Type"),
                build_types,
                0,
                editable=False)
            if not ok:
                return
            build_type = value

        url = build_urls[build_type]

        u = urllib.parse.urlparse(url)
        default_filename = os.path.basename(u.path)
        filename = self.get_firmware_save_file(default_filename)
        if not filename:
            return

        firmware_bytes = self.firmware_cache.get(url, None)
        if firmware_bytes and isinstance(firmware_bytes, bytes):
            logger.info("Using cached firmware from %s", url)
            with open(filename, "wb") as f:
                f.write(firmware_bytes)
        else:
            logger.info("Downloading firmware from %s", url)

            self.update_progress.setMinimum(0)
            self.update_progress.setMaximum(0)
            self.update_progress.setValue(0)
            self.update_progress.setLabelText(
                self.tr("Downloading firmware..."))
            self.update_progress.forceShow()

            file = open(filename, "w+b")
            self.firmware_downloader.start_download(url, file)

    @QtCore.Slot(object, str)
    def firmware_download_error(self, file: BinaryIO, error_str: str) -> None:
        self.update_progress.reset()
        file.close()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)
        os.unlink(file.filename)  # type: ignore

    @QtCore.Slot(str, object)
    def firmware_download_completed(self, url: str, file: BinaryIO) -> None:
        self.update_progress.reset()
        try:
            file.seek(0)
            firmware_bytes = file.read()
        except Exception:
            firmware_bytes = None
        finally:
            file.close()

        if firmware_bytes:
            self.firmware_cache.set(url, firmware_bytes)

        QtWidgets.QMessageBox.information(self, self.tr("Finished"),
                                          self.tr("Finished download"))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        geometry = self.saveGeometry()
        self.settings.setValue('Geometry', geometry)

        QtWidgets.QWidget.closeEvent(self, event)

    @QtCore.Slot(object)
    def controller_created(self, controller: DeviceController) -> None:
        # find the parent tree item, if any
        parent_tree_item = None
        parent_controller = controller.parent_controller
        if parent_controller is not None:
            parent_widget = self.get_tab_widget(parent_controller)
            if parent_widget is not None:
                parent_tree_item = self.tab_tree_items.get(parent_widget, None)
        if parent_tree_item is None:
            parent = self.treeWidget
        else:
            parent = parent_tree_item

        # create a tree item for the controller
        tree_item = QtWidgets.QTreeWidgetItem(parent)
        tree_item.setExpanded(True)
        tree_item.setText(0, controller.serial_number)
        tree_item.setIcon(0, self.connecting_icon)

        # create the tab widget
        tab_widget = DeviceTab(controller, self, self.preferences,
                               self.collapsed, self.firmware_cache, tree_item)

        # update tree item data
        self.tab_tree_items[tab_widget] = tree_item
        tree_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, tab_widget)

        # find the insertion index
        def sort_key(tab_widget: DeviceTab) -> str:
            def controller_key(controller: DeviceController) -> str:
                if controller.parent_controller:
                    base = controller_key(controller.parent_controller)
                    return ".".join((base, controller.serial_number))
                else:
                    return controller.serial_number

            return controller_key(tab_widget.controller)

        index = bisect.bisect(self.tab_widgets, sort_key(tab_widget),
                              key=sort_key)

        self.tab_widgets.insert(index, tab_widget)
        self.tabWidget.insertTab(index + 1, tab_widget, self.connecting_icon,
                                 controller.serial_number)

        tab_widget.collapsed_set.connect(self.collapsed_set)

        # show it (if the user created it)
        if tab_widget.controller.get_manual_control():
            self.tabWidget.setCurrentWidget(tab_widget)

        self.stackedWidget.setCurrentIndex(0)

    def get_tab_widget(self,
                       controller: DeviceController) -> Optional[DeviceTab]:
        for tab_widget in self.tab_widgets:
            if tab_widget.controller == controller:
                return tab_widget
        return None

    @QtCore.Slot(object)
    def remove_controller(self, controller: DeviceController) -> None:
        tab_widget = self.get_tab_widget(controller)
        if not tab_widget:
            return

        try:
            if self.shown_tab == tab_widget:
                self.shown_tab = None
            index = self.tab_widgets.index(tab_widget)
            self.tab_widgets.pop(index)
            self.tabWidget.removeTab(index + 1)
        except ValueError:
            pass

        tab_widget.deleteLater()

        if len(self.tab_widgets) == 0:
            self.stackedWidget.setCurrentIndex(1)
            self.logo_animation.start()

        # remove from the tree
        tree_item = self.tab_tree_items.pop(tab_widget, None)
        if tree_item is not None:
            parent = tree_item.parent()
            if parent is not None:
                parent.removeChild(tree_item)
            else:
                self.treeWidget.takeTopLevelItem(
                    self.treeWidget.indexOfTopLevelItem(tree_item))
            children = tree_item.takeChildren()
            if children:
                logger.warning("tree item still has children: %s", children)

    def update_device_name(self, widget: DeviceTab, name: str) -> None:
        try:
            index = self.tab_widgets.index(widget)
            self.tabWidget.setTabText(index + 1, name)
        except ValueError:
            pass

    def set_tab_connected(self, widget: DeviceTab) -> None:
        try:
            index = self.tab_widgets.index(widget)
            self.tabWidget.setTabIcon(index + 1, self.connected_icon)
            tree_item = self.tab_tree_items.get(widget, None)
            if tree_item is not None:
                tree_item.setIcon(0, self.connected_icon)

            parent_controller = widget.controller.parent_controller
            if parent_controller is not None:
                parent_widget = self.get_tab_widget(parent_controller)
                if parent_widget is not None:
                    # show the child widget if we're focused on the parent
                    self.show_tab(widget, parent_widget)
        except ValueError:
            pass

    def set_tab_disconnected(self, widget: DeviceTab) -> None:
        try:
            index = self.tab_widgets.index(widget)
            self.tabWidget.setTabIcon(index + 1, self.connecting_icon)
            tree_item = self.tab_tree_items.get(widget, None)
            if tree_item is not None:
                tree_item.setIcon(0, self.connecting_icon)
        except ValueError:
            pass

    def show_tab(self, widget: DeviceTab,
                 src: Optional[DeviceTab] = None) -> None:
        if src and self.tabWidget.currentWidget() != src:
            return  # source is not currently displayed
        self.tabWidget.setCurrentWidget(widget)

    @QtCore.Slot()
    def show_about(self) -> None:
        dialog = AboutDialog(self)
        try:
            dialog.exec()
        finally:
            dialog.deleteLater()

    def get_html_dir(self) -> str:
        is_frozen = getattr(sys, 'frozen', False)
        if is_frozen:
            # load the build_info.txt
            return os.path.join(os.path.dirname(sys.executable), "html")
        else:
            return os.path.join(os.path.dirname(__file__), "html")

    @QtCore.Slot()
    def show_channel_table(self) -> None:
        filename = os.path.join(self.get_html_dir(), "asphodel_channels.html")
        url = QtCore.QUrl.fromLocalFile(filename)
        QtGui.QDesktopServices.openUrl(url)

    def show_file_on_disk(self, file: str) -> None:
        file = os.path.abspath(file)
        if sys.platform == "win32":
            subprocess.Popen(['explorer', '/select,', file])
        elif sys.platform == "darwin":
            args = [
                "osascript",
                "-e",
                'tell application "Finder"',
                "-e",
                "activate",
                "-e",
                f'select POSIX file "{file}"',
                "-e",
                "end tell",
            ]
            subprocess.Popen(args)
        else:
            url = QtCore.QUrl.fromLocalFile(os.path.dirname(file))
            QtGui.QDesktopServices.openUrl(url)

    @QtCore.Slot()
    def show_log_dir(self) -> None:
        logdir = os.path.abspath(
            QtCore.QStandardPaths.writableLocation(
                QtCore.QStandardPaths.StandardLocation.AppLocalDataLocation))
        logfile = os.path.join(logdir, "main.log")

        self.show_file_on_disk(logfile)

    @QtCore.Slot()
    def show_config_dir(self) -> None:
        config = self.preferences.settings.fileName()
        if os.path.exists(config):
            self.show_file_on_disk(config)

    @QtCore.Slot()
    def set_disable_streaming(self) -> None:
        disable_streaming = self.actionDisableStreaming.isChecked()
        self.dispatcher.set_disable_streaming(disable_streaming)

    @QtCore.Slot()
    def set_disable_archiving(self) -> None:
        disable_archiving = self.actionDisableArchiving.isChecked()
        self.warningLabel.setVisible(disable_archiving)
        self.dispatcher.set_disable_archiving(disable_archiving)

    @QtCore.Slot()
    def show_preferences(self) -> None:
        dialog = PreferencesDialog(self.preferences, self)
        try:
            if dialog.exec():
                self.dispatcher.update_preferences()
                for device_tab in self.tab_widgets:
                    device_tab.update_preferences()
        finally:
            dialog.deleteLater()

    @QtCore.Slot()
    def update_datetime_label(self) -> None:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
        s = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.datetimeLabel.setText(s)

    @QtCore.Slot(bool, float)
    def rate_status_cb(self, uploading: bool, rate: float) -> None:
        if uploading:
            # uploading ongoing
            self.uploadRateLabel.setText("{:.1f} KB/s".format(rate / 1000))
        else:
            # uploading finished
            self.uploadRateLabel.setText("0.0 KB/s")
            self.upload_timeout_timer.start(1000)  # 1 second until hide

    @QtCore.Slot(str, object, object)
    def upload_status_cb(self, filename: str, sent_bytes: int,
                         total_bytes: int) -> None:
        # uploading starting
        self.uploadNameLabel.setText(filename)
        self.uploadProgress.setVisible(True)
        self.uploadProgress.setRange(0, total_bytes)
        self.uploadProgress.setValue(sent_bytes)
        self.upload_timeout_timer.stop()

    @QtCore.Slot()
    def upload_timeout_cb(self) -> None:
        self.uploadProgress.setVisible(False)
        self.uploadNameLabel.setText("Waiting for file to upload")

    @QtCore.Slot()
    def upload_manager_error(self) -> None:
        self.uploadNameLabel.setText("Error")
        msg = "Error connecting. Check upload configuration."
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), self.tr(msg))

    @QtCore.Slot()
    def closable_tabs_cb(self) -> None:
        new_value = self.actionClosableTabs.isChecked()
        self.tabWidget.setTabsClosable(new_value)
        self.preferences.closeable_tabs = new_value

        if new_value:
            tab_bar = self.tabWidget.tabBar()
            tab_bar.setTabButton(0, QtWidgets.QTabBar.ButtonPosition.LeftSide,
                                 None)  # type: ignore
            tab_bar.setTabButton(0, QtWidgets.QTabBar.ButtonPosition.RightSide,
                                 None)  # type: ignore

    @QtCore.Slot(int)
    def tab_close_requested(self, index: int) -> None:
        if index <= 0:
            return  # can't close the device tab
        widget = self.tab_widgets[index - 1]
        widget.close_controller()

    @QtCore.Slot(QtWidgets.QTreeWidgetItem, int)
    def tree_item_double_clicked(self, item: QtWidgets.QTreeWidgetItem,
                                 col: int) -> None:
        tab_widget = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if tab_widget is not None:
            self.show_tab(tab_widget)

    @QtCore.Slot()
    def mark_directory(self) -> None:
        # ask the user for the file name
        output_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, self.tr("Select Directory"), self.preferences.base_dir)

        if not output_dir:
            return

        # search the directory for .apd files
        collected_files: list[str] = []
        for root, _dirs, files in os.walk(output_dir):
            for name in files:
                if name.endswith(".apd"):
                    apd_filename = os.path.join(root, name)
                    collected_files.append(apd_filename)

        self.dispatcher.mark_for_upload(collected_files)

    @QtCore.Slot()
    def mark_files(self) -> None:
        # ask the user for the file name
        file_filter = self.tr("Data Files (*.apd)")
        val = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                     self.tr("Select Files"),
                                                     self.preferences.base_dir,
                                                     file_filter)
        files = val[0]

        self.dispatcher.mark_for_upload(files)

    @QtCore.Slot()
    def next_tab(self) -> None:
        new_index = self.tabWidget.currentIndex() + 1
        if new_index >= self.tabWidget.count():
            new_index = 1  # skip the "devices" tab
        self.tabWidget.setCurrentIndex(new_index)

    @QtCore.Slot()
    def prev_tab(self) -> None:
        new_index = self.tabWidget.currentIndex() - 1
        if new_index < 1:  # skip the "devices" tab
            new_index = self.tabWidget.count() - 1
        self.tabWidget.setCurrentIndex(new_index)

    @QtCore.Slot(bool)
    def collapsed_set(self, collapsed: bool) -> None:
        self.collapsed = collapsed
        self.preferences.collapsed = collapsed
        for tab_widget in self.tab_widgets:
            tab_widget.set_collapsed(collapsed)

    @QtCore.Slot(int)
    def current_tab_changed_cb(self, index: int) -> None:
        if index == -1 or index == 0:
            new_tab = None
        else:
            new_tab = self.tab_widgets[index - 1]

        if self.shown_tab == new_tab:
            return  # no change

        if self.shown_tab is not None:
            self.shown_tab.set_is_shown(False)
        if new_tab is not None:
            new_tab.set_is_shown(True)

        self.shown_tab = new_tab

    @QtCore.Slot(int, int)
    def rf_power_changed_cb(self, enabled: int, total: int) -> None:
        disabled = max(0, total - enabled)

        enable_text = self.tr("Enable RF Power ({})").format(disabled)
        self.actionEnableRFPower.setText(enable_text)
        self.actionEnableRFPower.setEnabled(disabled > 0)

        disable_text = self.tr("Disable RF Power ({})").format(enabled)
        self.actionDisableRFPower.setText(disable_text)
        self.actionDisableRFPower.setEnabled(enabled > 0)

    @QtCore.Slot()
    def find_tcp_devices(self, *, initial_devices: Optional[
            list[asphodel.AsphodelNativeDevice]] = None) -> None:
        dialog = TCPScanDialog(self.dispatcher, self.preferences,
                               initial_devices, self)
        try:
            ret = dialog.exec()
            if ret == 0:
                return

            devices = dialog.get_selected_devices()
        finally:
            dialog.deleteLater()

        for device in devices:
            self.dispatcher.create_tcp_proxy_from_device(device)

    def connect_tcp_device_error(self) -> None:
        QtWidgets.QMessageBox.critical(self, self.tr("Error"),
                                       self.tr("Could not connect to device!"))

    @QtCore.Slot()
    def connect_tcp_device(self) -> None:
        dialog = TCPConnectDialog(self)
        try:
            ret = dialog.exec()
            if ret == 0:
                return  # user cancelled

            results = dialog.get_results()
        finally:
            dialog.deleteLater()

        self.dispatcher.create_manual_tcp_proxy(
            hostname=results['hostname'],
            port=results['port'],
            timeout=1000,
            serial_number=results['serial_number'],
            err_cb=self.connect_tcp_device_error,
        )

    @QtCore.Slot(bool, object)
    def initial_devices_connected_cb(
            self, tcp_scanned: bool,
            tcp_devices: list[asphodel.AsphodelNativeDevice]) -> None:
        if self.tab_widgets:
            self.show_tab(self.tab_widgets[0])
            return  # already have devices, no need to show dialogs

        if not tcp_scanned:
            tcp_devices = asphodel.find_tcp_devices()

        if tcp_devices:
            self.find_tcp_devices(initial_devices=tcp_devices)

    @QtCore.Slot(object)
    def upload_manager_changed_cb(
            self, upload_manager: Optional[S3UploadManager]) -> None:
        if upload_manager:
            self.uploadRateLabel.setVisible(True)
            self.uploadProgress.setVisible(False)  # hide when inactive
            self.uploadNameLabel.setVisible(True)
            self.uploadRateLabel.setText("0.0 kB/s")
            self.uploadNameLabel.setText("Waiting for file to upload")

            upload_manager.rate_status.connect(self.rate_status_cb)
            upload_manager.upload_status.connect(self.upload_status_cb)
            upload_manager.error.connect(self.upload_manager_error)
        else:
            # no upload configured, hide associated widgets
            self.uploadRateLabel.setVisible(False)
            self.uploadProgress.setVisible(False)
            self.uploadNameLabel.setVisible(False)

    @QtCore.Slot(str)
    def schedule_error_cb(self, error: str) -> None:
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), error)

    @QtCore.Slot(str)
    def schedule_warning_cb(self, warning: str) -> None:
        QtWidgets.QMessageBox.warning(self, self.tr("Warning"), warning)

    @QtCore.Slot()
    def reload_schedule_cb(self) -> None:
        self.schedule_reader.reload()

    @QtCore.Slot(object)
    def active_triggers_changed(self, active_triggers: frozenset[str]) -> None:
        if active_triggers:
            active_trigger_str = self.tr("Active triggers: {}")
            s = active_trigger_str.format(
                ", ".join(sorted(active_triggers, key=str.casefold)))
            self.activeTriggerLabel.setText(s)
            self.activeTriggerLabel.setVisible(True)
        else:
            self.activeTriggerLabel.setVisible(False)
