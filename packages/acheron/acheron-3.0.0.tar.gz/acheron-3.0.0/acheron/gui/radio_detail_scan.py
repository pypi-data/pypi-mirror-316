from collections import deque
from dataclasses import dataclass, fields
import datetime
import logging
from typing import Any, cast, Optional

from PySide6 import QtCore, QtGui, QtWidgets

from asphodel.device_info import ActiveScanInfo

from ..core.device_controller import DeviceController
from ..core.preferences import Preferences
from ..core.radio_scan import ActiveScanDatabase, ScanResult
from .ui.ui_detail_scan_dialog import Ui_DetailScanDialog

logger = logging.getLogger(__name__)


class SortableTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __init__(self) -> None:
        super().__init__()
        self.sort_value: Any = None

    def __lt__(self, other: QtWidgets.QTableWidgetItem) -> bool:
        try:
            other_sort_value: Any = other.sort_value  # type: ignore
            if other_sort_value is not None and self.sort_value is not None:
                return self.sort_value < other_sort_value
        except AttributeError:
            pass
        # fall back
        return self.text() < other.text()


@dataclass()
class TableItems:
    serial_number: SortableTableWidgetItem
    scan_strength: SortableTableWidgetItem
    tag1: QtWidgets.QTableWidgetItem
    tag2: QtWidgets.QTableWidgetItem
    board_info: QtWidgets.QTableWidgetItem
    build_info: QtWidgets.QTableWidgetItem
    build_date: QtWidgets.QTableWidgetItem
    bootloader: QtWidgets.QTableWidgetItem
    device_mode: QtWidgets.QTableWidgetItem
    last_seen: SortableTableWidgetItem


@dataclass()
class RowInformation:
    table_items: TableItems
    scan: ScanResult
    last_seen_seconds: Optional[int]
    connected_radio: Optional[str]  # serial number


class DetailScanDialog(Ui_DetailScanDialog, QtWidgets.QDialog):
    def __init__(self, active_scan_database: ActiveScanDatabase,
                 preferences: Preferences,
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.active_scan_database = active_scan_database
        self.preferences = preferences

        self.row_info: dict[int, RowInformation] = {}  # key: serial_number
        self.scans_to_process: deque[ScanResult] = deque()

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup()

        self.selection_changed()

    def extra_ui_setup(self) -> None:
        self.bootloader_fg_brush = QtGui.QBrush(
            QtGui.QColor(QtCore.Qt.GlobalColor.black))
        self.bootloader_bg_brush = QtGui.QBrush(
            QtGui.QColor(QtCore.Qt.GlobalColor.yellow))
        self.stale_fg_brush = QtGui.QBrush(
            QtGui.QColor(QtCore.Qt.GlobalColor.black))
        self.stale_bg_brush = QtGui.QBrush(
            QtGui.QColor(QtCore.Qt.GlobalColor.yellow))
        self.old_fg_brush = QtGui.QBrush(
            QtGui.QColor(QtCore.Qt.GlobalColor.black))
        self.old_bg_brush = QtGui.QBrush(
            QtGui.QColor(QtCore.Qt.GlobalColor.red))

        self.default_font = QtGui.QFont()
        self.bootloader_font = QtGui.QFont()
        self.bootloader_font.setBold(True)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.clearButton = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Reset)
        self.clearButton.setText(self.tr("Clear"))
        self.clearButton.clicked.connect(self.clear_button_cb)

        self.active_scan_database.cleared.connect(self.database_cleared)
        self.active_scan_database.active_scan_ready.connect(
            self.update_active_scan_info)
        self.active_scan_database.remote_connecting.connect(
            self.update_controller)

        self.backgroundActiveScan.toggled.connect(
            self.set_background_active_scan)
        self.backgroundActiveScan.setChecked(
            self.preferences.background_active_scan)

        selection_model = self.tableWidget.selectionModel()
        selection_model.selectionChanged.connect(self.selection_changed)
        self.tableWidget.doubleClicked.connect(self.double_click_cb)

        self.tableWidget.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.tableWidget.setSortingEnabled(True)

        self.update_timer = QtCore.QTimer(self)
        self.update_timer.timeout.connect(self.update_rows)
        self.update_timer.start(500)

        self.update_scan_count()

    @QtCore.Slot()
    def set_background_active_scan(self) -> None:
        if self.backgroundActiveScan.isChecked():
            self.preferences.background_active_scan = True
        else:
            self.preferences.background_active_scan = False

    @QtCore.Slot()
    def double_click_cb(self) -> None:
        self.accept()

    def get_selected_scan(self) -> Optional[ScanResult]:
        rows = self.tableWidget.selectionModel().selectedRows()
        if rows:
            row = rows[0].row()
            item = cast(SortableTableWidgetItem, self.tableWidget.item(row, 0))
            serial_number = item.sort_value
            if serial_number:
                return self.row_info[serial_number].scan

        return None

    @QtCore.Slot()
    def selection_changed(self) -> None:
        ok_button = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Ok)
        if self.tableWidget.selectionModel().hasSelection():
            ok_button.setEnabled(True)
        else:
            ok_button.setEnabled(False)

    @QtCore.Slot()
    def database_cleared(self) -> None:
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.row_info.clear()
        self.scans_to_process.clear()
        self.update_scan_count()

    @QtCore.Slot()
    def clear_button_cb(self) -> None:
        self.active_scan_database.clear_database()

    def handle_scan(self, scan: ScanResult) -> None:
        row_info = self.row_info.get(scan.serial_number)
        if not row_info:
            table_items = self.add_row(scan.serial_number)
            self.update_table_items(table_items, scan, None)

            row_info = RowInformation(table_items, scan, None, None)
            self.row_info[scan.serial_number] = row_info
            self.update_scan_count()

            controller = self.active_scan_database.get_remote_controller(
                scan.serial_number)
            if controller:
                self.update_controller(scan.serial_number, controller)

            active_scan = self.active_scan_database.get_active_scan(
                scan.serial_number)
            if active_scan:
                self.update_active_scan_info(scan.serial_number, active_scan)

            self.update_last_seen(row_info)
        else:
            self.scans_to_process.append(scan)

    def update_table_items(self, table_items: TableItems, new_scan: ScanResult,
                           old_scan: Optional[ScanResult]) -> None:
        if (old_scan is None or
                old_scan.scan_strength != new_scan.scan_strength):
            if new_scan.scan_strength is not None:
                # update scan strength
                scan_strength = table_items.scan_strength
                scan_strength.sort_value = new_scan.scan_strength
                scan_strength.setText("{} dBm".format(new_scan.scan_strength))

        if old_scan is None or old_scan.device_mode != new_scan.device_mode:
            # update device mode
            device_mode = table_items.device_mode
            device_mode.setData(QtCore.Qt.ItemDataRole.DisplayRole,
                                new_scan.device_mode)

        if old_scan is None or old_scan.bootloader != new_scan.bootloader:
            bootloader = table_items.bootloader
            if new_scan.bootloader:
                bootloader.setData(
                    QtCore.Qt.ItemDataRole.DisplayRole, "Running")
                bootloader.setFont(self.bootloader_font)

                for field in fields(table_items):
                    item = getattr(table_items, field.name)
                    item.setForeground(self.bootloader_fg_brush)
                    item.setBackground(self.bootloader_bg_brush)
            else:
                bootloader.setData(QtCore.Qt.ItemDataRole.DisplayRole, "")
                bootloader.setFont(self.default_font)

                for field in fields(table_items):
                    item = getattr(table_items, field.name)
                    item.setData(QtCore.Qt.ItemDataRole.ForegroundRole, None)
                    item.setData(QtCore.Qt.ItemDataRole.BackgroundRole, None)

    def add_row(self, serial_number: int) -> TableItems:
        start_index = self.tableWidget.rowCount()
        self.tableWidget.insertRow(start_index)

        serial_number_item = SortableTableWidgetItem()
        serial_number_item.sort_value = serial_number
        serial_number_item.setData(
            QtCore.Qt.ItemDataRole.DisplayRole, serial_number)
        self.tableWidget.setItem(start_index, 0, serial_number_item)

        table_items: list[QtWidgets.QTableWidgetItem] = [serial_number_item]

        for i in range(1, self.tableWidget.columnCount()):
            new_item: QtWidgets.QTableWidgetItem
            if i in (1, 9):
                new_item = SortableTableWidgetItem()
            else:
                new_item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(serial_number_item.row(), i, new_item)
            table_items.append(new_item)

        return TableItems(*table_items)  # type: ignore

    def update_last_seen(self, row_info: RowInformation,
                         now: Optional[datetime.datetime] = None) -> None:
        if now is None:
            now = datetime.datetime.now(datetime.timezone.utc)

        delta = now - row_info.scan.last_seen
        item = row_info.table_items.last_seen
        item.sort_value = delta

        seconds = int(delta.total_seconds())

        if seconds != row_info.last_seen_seconds:
            row_info.last_seen_seconds = seconds
            if seconds == 1:
                text = "1 second ago"
            else:
                text = "".join((str(seconds), " seconds ago"))
            item.setText(text)

            if seconds < 10:
                # normal
                if row_info.scan.bootloader:
                    item.setForeground(self.bootloader_fg_brush)
                    item.setBackground(self.bootloader_bg_brush)
                else:
                    # go back to default
                    item.setData(QtCore.Qt.ItemDataRole.ForegroundRole, None)
                    item.setData(QtCore.Qt.ItemDataRole.BackgroundRole, None)
            elif seconds < 30:
                item.setForeground(self.stale_fg_brush)
                item.setBackground(self.stale_bg_brush)
            else:
                item.setForeground(self.old_fg_brush)
                item.setBackground(self.old_bg_brush)

    @QtCore.Slot()
    def update_rows(self) -> None:
        self.tableWidget.setUpdatesEnabled(False)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)

        try:
            while True:
                scan = self.scans_to_process.popleft()
                row_info = self.row_info.get(scan.serial_number)
                if row_info:
                    old_scan = row_info.scan
                    self.update_table_items(
                        row_info.table_items, scan, old_scan)
                    row_info.scan = scan
        except IndexError:
            pass

        now = datetime.datetime.now(datetime.timezone.utc)
        for row_info in self.row_info.values():
            if row_info.connected_radio:
                # skip connected ones
                continue

            self.update_last_seen(row_info, now)

        header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.setUpdatesEnabled(True)

    @QtCore.Slot(int, object)
    def update_active_scan_info(self, remote: int,
                                active_scan: ActiveScanInfo) -> None:
        row_info = self.row_info.get(remote)
        if row_info is None:
            return

        # add active scan information
        user_tag_1 = active_scan.user_tag_1
        if user_tag_1 is None:
            user_tag_1 = ""
        row_info.table_items.tag1.setText(user_tag_1)
        user_tag_2 = active_scan.user_tag_2
        if user_tag_2 is None:
            user_tag_2 = ""
        row_info.table_items.tag2.setText(user_tag_2)

        board_info_str = "{} rev {}".format(*active_scan.board_info)
        row_info.table_items.board_info.setText(board_info_str)
        row_info.table_items.build_info.setText(active_scan.build_info)
        row_info.table_items.build_date.setText(active_scan.build_date)

    @QtCore.Slot(int, object)
    def update_controller(self, remote: int,
                          controller: Optional[DeviceController]) -> None:
        row_info = self.row_info.get(remote)
        if row_info is None:
            return

        old_connected_radio = row_info.connected_radio

        if controller:
            row_info.connected_radio = controller.serial_number
        else:
            row_info.connected_radio = None

        if old_connected_radio == row_info.connected_radio:
            # nothing is new
            return

        if row_info.connected_radio:
            item = row_info.table_items.last_seen
            item.setText("Connected to {}".format(row_info.connected_radio))

            if row_info.scan.bootloader:
                item.setForeground(self.bootloader_fg_brush)
                item.setBackground(self.bootloader_bg_brush)
            else:
                # go back to default
                item.setData(QtCore.Qt.ItemDataRole.ForegroundRole, None)
                item.setData(QtCore.Qt.ItemDataRole.BackgroundRole, None)
        else:
            self.update_last_seen(row_info)

    def update_scan_count(self) -> None:
        self.clearButton.setText("Clear ({})".format(len(self.row_info)))
