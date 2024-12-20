from __future__ import annotations
import bisect
from collections import deque
import datetime
import logging
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

from ..device_logging import DeviceLoggerAdapter

from ..core.device_controller import DeviceController, DeviceControllerState
from ..core.preferences import Preferences
from ..core.radio_scan import ActiveScanDatabase, ScanResult
from .radio_detail_scan import DetailScanDialog
from .ui.ui_radio_panel import Ui_RadioPanel


logger = logging.getLogger(__name__)


class RadioPanel(Ui_RadioPanel, QtWidgets.QGroupBox):
    show_remote_clicked = QtCore.Signal()

    def __init__(self, controller: DeviceController,
                 active_scan_database: ActiveScanDatabase,
                 preferences: Preferences,
                 parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.controller = controller
        self.active_scan_database = active_scan_database
        self.preferences = preferences

        self.logger = DeviceLoggerAdapter(logger, controller.serial_number)

        self.scan_serials: list[int] = []
        self.scans: dict[int, ScanResult] = {}
        self.device_list_additions: deque[
            tuple[int, QtWidgets.QListWidgetItem]] = deque()

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup()
        self.setup_callbacks()

    def extra_ui_setup(self) -> None:
        self.detail_scan_dialog = DetailScanDialog(
            self.active_scan_database, self.preferences, self)

        self.menu = QtWidgets.QMenu(self)
        self.menu.addAction(self.actionConnectNoStreaming)
        self.menu.addSeparator()
        self.menu.addAction(self.actionConnectSpecificBootloader)
        self.menu.addAction(self.actionConnectSpecificSerial)
        self.advancedMenuButton.setMenu(self.menu)

        self.deviceList.addAction(self.actionClear)

        self.actionClear.setIcon(QtGui.QIcon.fromTheme("delete"))
        self.clearButton.setDefaultAction(self.actionClear)

    def setup_callbacks(self) -> None:
        self.detailScanButton.clicked.connect(self.detail_scan)

        self.connectButton.clicked.connect(self.connect_button_cb)
        self.disconnectButton.clicked.connect(self.disconnect_button_cb)
        self.goToRemoteButton.clicked.connect(self.show_remote_clicked)

        self.deviceList.currentRowChanged.connect(self.current_row_changed_cb)
        self.deviceList.itemDoubleClicked.connect(
            self.item_double_clicked_cb)

        self.actionConnectNoStreaming.triggered.connect(
            self.connect_no_streaming_cb)
        self.actionConnectSpecificBootloader.triggered.connect(
            self.connect_specific_bootloader_cb)
        self.actionConnectSpecificSerial.triggered.connect(
            self.connect_specific_serial_cb)
        self.actionClear.triggered.connect(self.clear_list)

        self.update_device_list_timer = QtCore.QTimer(self)
        self.update_device_list_timer.timeout.connect(
            self.update_device_list)
        self.update_device_list_timer.start(250)

        self.controller.scan_data.connect(self.scan_data_cb)
        self.controller.remote_target_changed.connect(
            self.remote_target_changed_cb)
        self.controller.scan_first_pass.connect(self.scan_first_pass_cb)
        self.controller.state_changed_signal.connect(
            self.controller_state_changed_cb)
        self.controller.remote_connected.connect(self.remote_connected_cb)
        self.controller.remote_target_connected.connect(
            self.remote_target_connected_cb)

    def add_ctrl_var_widget(
            self, widget: QtWidgets.QWidget) -> None:  # called from device_tab
        self.ctrlVarLayout.addWidget(widget)

    def clear_ctrl_var_widgets(self) -> None:
        while True:
            item = self.ctrlVarLayout.takeAt(0)
            if not item:
                break
            # NOTE: the items are deleted by the caller

    @QtCore.Slot()
    def connect_button_cb(self) -> None:
        scan = self.get_selected_scan()
        if scan:
            self.controller.set_remote_target(
                scan.serial_number, scan.bootloader)

    @QtCore.Slot()
    def connect_no_streaming_cb(self) -> None:
        scan = self.get_selected_scan()
        if scan:
            self.controller.set_remote_target(
                scan.serial_number, scan.bootloader, streaming=False)

    @QtCore.Slot()
    def connect_specific_bootloader_cb(self) -> None:
        sn, ok = QtWidgets.QInputDialog.getInt(
            self, self.tr("Bootloader Serial"),
            self.tr("Input bootloader serial number"))
        if not ok:
            return

        self.controller.set_remote_target(sn, True)

    @QtCore.Slot()
    def connect_specific_serial_cb(self) -> None:
        sn, ok = QtWidgets.QInputDialog.getInt(
            self, self.tr("Device Serial"),
            self.tr("Input device serial number"))
        if not ok:
            return

        self.controller.set_remote_target(sn, False)

    @QtCore.Slot()
    def disconnect_button_cb(self) -> None:
        self.controller.clear_remote_target()

    @QtCore.Slot(object, bool, bool)
    def remote_target_changed_cb(self, serial_number: Optional[int],
                                 bootloader: bool, streaming: bool) -> None:
        if serial_number is None:
            self.actionConnectNoStreaming.setEnabled(True)
            self.actionConnectSpecificBootloader.setEnabled(True)
            self.actionConnectSpecificSerial.setEnabled(True)
            self.detailScanButton.setEnabled(True)
            self.deviceList.setEnabled(True)
            self.clearButton.setEnabled(True)
            self.disconnectButton.setEnabled(False)

            self.connectButton.setText(self.tr("Connect"))
            selected = self.get_selected_scan() is not None
            self.connectButton.setEnabled(selected)
        else:
            self.prune_list(serial_number, bootloader)

            self.actionConnectNoStreaming.setEnabled(False)
            self.actionConnectSpecificBootloader.setEnabled(False)
            self.actionConnectSpecificSerial.setEnabled(False)
            self.detailScanButton.setEnabled(False)
            self.deviceList.setEnabled(False)
            self.clearButton.setEnabled(False)
            self.disconnectButton.setEnabled(True)

            self.connectButton.setText(self.tr("Connecting..."))
            self.connectButton.setEnabled(False)

    @QtCore.Slot(bool)
    def remote_target_connected_cb(self, connected: bool) -> None:
        if connected:
            self.actionConnectNoStreaming.setEnabled(False)
            self.actionConnectSpecificBootloader.setEnabled(False)
            self.actionConnectSpecificSerial.setEnabled(False)
            self.detailScanButton.setEnabled(False)
            self.deviceList.setEnabled(False)
            self.clearButton.setEnabled(False)
            self.disconnectButton.setEnabled(True)

            self.connectButton.setText(self.tr("Connected"))
            self.connectButton.setEnabled(False)

    @QtCore.Slot(bool)
    def remote_connected_cb(self, connected: bool) -> None:
        self.goToRemoteButton.setEnabled(connected)

    @QtCore.Slot()
    def scan_first_pass_cb(self) -> None:
        self.update_device_list()
        if self.get_selected_scan() is None:
            if self.deviceList.count():
                self.deviceList.setCurrentRow(0)

    @QtCore.Slot(object, str)
    def controller_state_changed_cb(self, state: DeviceControllerState,
                                    _message: str) -> None:
        if state == DeviceControllerState.STREAMING_STARTING:
            self.clear_list()

    @QtCore.Slot()
    def detail_scan(self) -> None:
        # run the dialog
        self.active_scan_database.detail_scan_opened()
        try:
            ret = self.detail_scan_dialog.exec()
        finally:
            self.active_scan_database.detail_scan_closed()

        if ret == 0:
            return  # user canceled

        scan = self.detail_scan_dialog.get_selected_scan()
        if scan:
            self.controller.set_remote_target(
                scan.serial_number, scan.bootloader)

    @QtCore.Slot(int)
    def current_row_changed_cb(self, row: int = -1) -> None:
        if row == -1:
            self.connectButton.setEnabled(False)
        else:
            self.connectButton.setEnabled(True)

    @QtCore.Slot(QtWidgets.QListWidgetItem)
    def item_double_clicked_cb(self, item: QtWidgets.QListWidgetItem) -> None:
        self.handle_device_list_additions()
        row = self.deviceList.row(item)
        if row != -1:
            serial_number = self.scan_serials[row]
            scan = self.scans.get(serial_number)
            if scan:
                self.controller.set_remote_target(
                    scan.serial_number, scan.bootloader)

    def get_selected_scan(self) -> Optional[ScanResult]:
        self.handle_device_list_additions()

        row = self.deviceList.currentRow()
        if row == -1:
            return None
        else:
            serial_number = self.scan_serials[row]
            return self.scans.get(serial_number)

    @QtCore.Slot(object, object)
    def scan_data_cb(self, _controller: DeviceController,
                     scans: list[ScanResult]) -> None:
        for scan in scans:
            self.detail_scan_dialog.handle_scan(scan)
            self.scans[scan.serial_number] = scan

        if self.controller.remote_target_serial is None:
            changed_scan_count = False
            for scan in scans:
                # find the entry if it exists
                index = bisect.bisect_left(
                    self.scan_serials, scan.serial_number)
                if (index != len(self.scan_serials) and
                        self.scan_serials[index] == scan.serial_number):
                    # don't update now, it'll get updated next timer pass
                    pass
                else:
                    # need to create a new entry
                    list_item = QtWidgets.QListWidgetItem()
                    self.update_list_item(list_item, scan)
                    self.scan_serials.insert(index, scan.serial_number)
                    self.device_list_additions.append((index, list_item))
                    changed_scan_count = True

            if changed_scan_count:
                self.update_scan_count()

    @staticmethod
    def _get_scan_strength_bars(scan_strength: int) -> str:
        if scan_strength >= -30:
            return "\u2581\u200A\u2582\u200A\u2583\u200A\u2585\u200A\u2587"
        elif scan_strength >= -40:
            return "\u2581\u200A\u2582\u200A\u2583\u200A\u2585\u200A\u2581"
        elif scan_strength >= -50:
            return "\u2581\u200A\u2582\u200A\u2583\u200A\u2581\u200A\u2581"
        elif scan_strength >= -60:
            return "\u2581\u200A\u2582\u200A\u2583\u200A\u2581\u200A\u2581"
        else:
            return "\u2581\u200A\u2581\u200A\u2581\u200A\u2581\u200A\u2581"

    def update_list_item(self, list_item: QtWidgets.QListWidgetItem,
                         scan: ScanResult) -> None:
        text_elements = []

        active_scan = self.active_scan_database.get_active_scan(
            scan.serial_number)

        if scan.serial_number != (-1 & 0xFFFFFFFF):
            text_elements.append(str(scan.serial_number))
        else:
            text_elements.append("Any")

        if scan.serial_number == self.controller.default_remote_target:
            text_elements.append("<Auto>")

        if self.controller.remote_target_serial is None:
            now = datetime.datetime.now(datetime.timezone.utc)
            if scan.scan_strength is not None:
                if (now - scan.last_seen).total_seconds() >= 5:
                    # stale
                    text_elements.append("(?)")
                else:
                    bars = self._get_scan_strength_bars(scan.scan_strength)
                    text_elements.append(f"({bars} {scan.scan_strength} dBm)")

        if scan.bootloader:
            text_elements.append("bootloader")

        if active_scan and active_scan.user_tag_1:
            text_elements.append("-")
            text_elements.append(f'"{active_scan.user_tag_1}"')
        elif scan.board_info:
            text_elements.append("-")
            text_elements.append(scan.board_info[0])

        list_item.setText(" ".join(text_elements))

    def _get_placeholder_scan(self, serial_number: int,
                              bootloader: bool) -> ScanResult:
        scan = self.scans.get(serial_number)
        if scan:
            return scan

        now = datetime.datetime.now(datetime.timezone.utc)

        scan = ScanResult(
            serial_number=serial_number,
            last_seen=now,
            bootloader=bootloader,
            asphodel_type=0,
            device_mode=0,
            scan_strength=None,
            board_info=None
        )

        self.scans[serial_number] = scan

        return scan

    def prune_list(self, connected_serial: Optional[int],
                   connected_bootloader: bool) -> None:
        self.deviceList.clear()
        self.scan_serials.clear()
        self.device_list_additions.clear()

        restore_scans: dict[int, ScanResult] = {}

        if connected_serial:
            scan = self._get_placeholder_scan(
                connected_serial, connected_bootloader)
            scan.scan_strength = None  # clear any old strength
            restore_scans[connected_serial] = scan

        if self.controller.default_remote_target:
            if self.controller.default_remote_target != connected_serial:
                scan = self._get_placeholder_scan(
                    self.controller.default_remote_target, False)
                scan.scan_strength = None  # clear any old strength
                scan.bootloader = False  # the default isn't a bootloader
                restore_scans[self.controller.default_remote_target] = scan

        for i, (serial_number) in enumerate(sorted(restore_scans.keys())):
            scan = restore_scans[serial_number]
            list_item = QtWidgets.QListWidgetItem()
            self.update_list_item(list_item, scan)

            self.scan_serials.append(scan.serial_number)
            self.deviceList.insertItem(i, list_item)

            if serial_number == connected_serial:
                self.deviceList.setCurrentRow(i)

        self.update_scan_count()

    @QtCore.Slot()
    def clear_list(self) -> None:
        self.prune_list(None, False)

    def update_scan_count(self) -> None:
        text = "Clear ({})".format(len(self.scan_serials))
        self.clearButton.setText(text)
        self.clearButton.setToolTip(text)

    def handle_device_list_additions(self) -> None:
        updated = False
        try:
            while True:
                index, list_item = self.device_list_additions.popleft()

                if not updated:
                    updated = True
                    self.deviceList.setUpdatesEnabled(False)

                self.deviceList.insertItem(index, list_item)
        except IndexError:
            pass

        if updated:
            self.deviceList.setUpdatesEnabled(True)

    @QtCore.Slot()
    def update_device_list(self) -> None:
        self.handle_device_list_additions()

        if self.controller.remote_target_serial is None:
            for index, serial_number in enumerate(self.scan_serials):
                list_item = self.deviceList.item(index)
                scan = self.scans.get(serial_number)
                if scan:
                    self.update_list_item(list_item, scan)
