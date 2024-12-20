import collections
import logging
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

import asphodel

from ..core.dispatcher import Dispatcher
from ..core.preferences import Preferences
from .ui.ui_tcp_scan_dialog import Ui_TCPScanDialog

logger = logging.getLogger(__name__)


class SortableTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __init__(self) -> None:
        super().__init__()
        self.sort_value: Optional[str] = None

    def __lt__(self, other: QtWidgets.QTableWidgetItem) -> bool:
        try:
            other_sort_value = other.sort_value  # type: ignore
            if other_sort_value is not None and self.sort_value is not None:
                return self.sort_value < other_sort_value
        except AttributeError:
            pass
        # fall back
        return self.text() < other.text()


TableItems = collections.namedtuple(
    "TableItems", ["serial_number", "tag1", "tag2", "board_info", "build_info",
                   "build_date", "bootloader", "available"])


class RowInformation:
    def __init__(self, table_items: TableItems):
        self.table_items = table_items
        self.device: Optional[asphodel.AsphodelNativeDevice] = None
        self.connected: bool = False


class TCPScanDialog(Ui_TCPScanDialog, QtWidgets.QDialog):
    def __init__(
            self, dispatcher: Dispatcher, preferences: Preferences,
            initial_devices: Optional[list[asphodel.AsphodelNativeDevice]],
            parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.dispatcher = dispatcher
        self.preferences = preferences

        self.row_info: dict[str, RowInformation] = {}  # key: serial_number

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup()

        if initial_devices is not None:
            self.update_devices(initial_devices)
        else:
            self.rescan()

    def extra_ui_setup(self) -> None:
        self.bootloader_fg_brush = QtGui.QBrush(
            QtGui.QColor(QtCore.Qt.GlobalColor.black))
        self.bootloader_bg_brush = QtGui.QBrush(
            QtGui.QColor(QtCore.Qt.GlobalColor.yellow))

        self.default_font = QtGui.QFont()
        self.bootloader_font = QtGui.QFont()
        self.bootloader_font.setBold(True)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.rescanButton = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Reset)
        self.rescanButton.setText(self.tr("Rescan"))
        self.rescanButton.clicked.connect(self.rescan)

        selection_model = self.tableWidget.selectionModel()
        selection_model.selectionChanged.connect(self.selection_changed)
        self.tableWidget.doubleClicked.connect(self.double_click_cb)

        self.tableWidget.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.tableWidget.setSortingEnabled(True)

        self.rescan_timer = QtCore.QTimer(self)
        self.rescan_timer.timeout.connect(self.rescan)

        self.automaticRescan.toggled.connect(self.set_automatic_rescan)
        self.automaticRescan.setChecked(self.preferences.automatic_rescan)

        self.finished.connect(self.rescan_timer.stop)

    @QtCore.Slot()
    def set_automatic_rescan(self) -> None:
        if self.automaticRescan.isChecked():
            self.preferences.automatic_rescan = True
            self.rescan_timer.start(1000)
        else:
            self.preferences.automatic_rescan = False
            self.rescan_timer.stop()

    @QtCore.Slot()
    def double_click_cb(self) -> None:
        self.accept()

    def get_selected_devices(self) -> list[asphodel.AsphodelNativeDevice]:
        selected_devices: list[asphodel.AsphodelNativeDevice] = []
        for index in self.tableWidget.selectionModel().selectedRows():
            row = index.row()
            item = self.tableWidget.item(row, 0)
            serial_number = item.sort_value  # type: ignore
            device = self.row_info[serial_number].device
            if device is not None:
                selected_devices.append(device)
        return selected_devices

    @QtCore.Slot()
    def selection_changed(self) -> None:
        ok_button = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Ok)
        if self.tableWidget.selectionModel().hasSelection():
            ok_button.setEnabled(True)
        else:
            ok_button.setEnabled(False)

    def update_row_with_device(self, row_info: RowInformation,
                               device: asphodel.AsphodelNativeDevice,
                               connected: bool) -> None:
        old_device = row_info.device
        row_info.device = device
        old_connected = row_info.connected
        row_info.connected = connected

        adv = device.tcp_get_advertisement()

        if (old_device is None or (connected != old_connected) or
                adv.connected != old_device.tcp_get_advertisement().connected):

            if connected:
                item_flags = QtCore.Qt.ItemFlag.NoItemFlags
                available_str = "No (tab already open)"
            elif adv.connected:
                item_flags = QtCore.Qt.ItemFlag.NoItemFlags
                available_str = "No (in use)"
            else:
                item_flags = (QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                available_str = "Yes"

            for item in row_info.table_items:
                item.setFlags(item_flags)

            row_info.table_items.available.setText(available_str)

        if old_device is None or (device.supports_bootloader_commands() !=
                                  old_device.supports_bootloader_commands()):
            item = row_info.table_items.bootloader
            if device.supports_bootloader_commands():
                item.setData(QtCore.Qt.ItemDataRole.DisplayRole, "Running")
                item.setFont(self.bootloader_font)

                for item in row_info.table_items:
                    item.setForeground(self.bootloader_fg_brush)
                    item.setBackground(self.bootloader_bg_brush)
            else:
                item.setData(QtCore.Qt.ItemDataRole.DisplayRole, "")
                item.setFont(self.default_font)

                for item in row_info.table_items:
                    item.setData(QtCore.Qt.ItemDataRole.ForegroundRole, None)
                    item.setData(QtCore.Qt.ItemDataRole.BackgroundRole, None)

        row_info.table_items.tag1.setText(adv.user_tag1)
        row_info.table_items.tag2.setText(adv.user_tag2)
        board_info_str = "{} rev {}".format(adv.board_type, adv.board_rev)
        row_info.table_items.board_info.setText(board_info_str)
        row_info.table_items.build_info.setText(adv.build_info)
        row_info.table_items.build_date.setText(adv.build_date)

    def add_row(self, serial_number: str) -> TableItems:
        start_index = self.tableWidget.rowCount()
        self.tableWidget.insertRow(start_index)

        serial_number_item = SortableTableWidgetItem()
        serial_number_item.sort_value = serial_number
        serial_number_item.setData(QtCore.Qt.ItemDataRole.DisplayRole,
                                   serial_number)
        self.tableWidget.setItem(start_index, 0, serial_number_item)

        table_items: list[QtWidgets.QTableWidgetItem] = [serial_number_item]

        for i in range(1, self.tableWidget.columnCount()):
            new_item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(serial_number_item.row(), i, new_item)
            table_items.append(new_item)

        return TableItems(*table_items)

    def remove_row(self, serial_number: str) -> None:
        row_info = self.row_info.pop(serial_number)
        serial_number_item = row_info.table_items.serial_number
        self.tableWidget.removeRow(serial_number_item.row())

    def update_devices(
            self, devices: list[asphodel.AsphodelNativeDevice]) -> None:
        connected_location_strs = self.dispatcher.get_proxy_locations()

        # add or update all devices in the list
        existing_serials = set()
        for device in devices:
            adv = device.tcp_get_advertisement()
            serial_number = adv.serial_number
            existing_serials.add(serial_number)

            location_str = device.get_location_string()
            connected = location_str in connected_location_strs

            row_info = self.row_info.get(serial_number)
            if not row_info:
                table_items = self.add_row(serial_number)
                row_info = RowInformation(table_items)
                self.row_info[serial_number] = row_info

            self.update_row_with_device(row_info, device, connected)

        # remove any old devices
        old_serials = set(self.row_info.keys())
        old_serials.difference_update(existing_serials)
        for serial_number in old_serials:
            self.remove_row(serial_number)

        self.selection_changed()

    @QtCore.Slot()
    def rescan(self) -> None:
        try:
            new_devices = asphodel.find_tcp_devices()
        except Exception:
            return
        self.update_devices(new_devices)
