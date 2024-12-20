import logging
import os
import re
from xml.dom.minidom import getDOMImplementation

from PySide6 import QtCore, QtGui, QtWidgets

import asphodel
from asphodel.device_info import DeviceInfo

from hyperborea.preferences import read_int_setting

from ..connectivity.modbus import get_numeric_serial
from ..calc_process.types import ChannelInformation
from ..core.preferences import DevicePreferences
from .ui.ui_connectivity_dialog import Ui_ConnectivityDialog

logger = logging.getLogger(__name__)


class ConnectivityDialog(Ui_ConnectivityDialog, QtWidgets.QDialog):
    def __init__(self, serial_number: str, device_info: DeviceInfo,
                 channel_info: dict[int, ChannelInformation],
                 device_prefs: DevicePreferences, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.serial_number = serial_number
        self.device_info = device_info
        self.numeric_serial_number = get_numeric_serial(serial_number)
        self.channel_info = channel_info
        self.device_prefs = device_prefs

        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.serial_number)

        self.setting_names: dict[str, tuple[QtWidgets.QCheckBox,
                                            QtWidgets.QSpinBox]] = {}

        self.setupUi(self)  # type: ignore

        self.add_channel_check_boxes()
        self.read_settings()

        self.accepted.connect(self.write_settings)
        self.modbusDetails.clicked.connect(self.show_modbus_details)

    def add_channel_check_boxes(self) -> None:
        pattern = re.compile("Channel([0-9]+)_([0-9]+)_Port")

        sort_keys: dict[str, tuple[int, int]] = {}

        total_channels = 0
        for channel_info in self.channel_info.values():
            for i, subchannel in enumerate(channel_info.subchannel_names):
                setting_name = "Channel{}_{}_Port".format(
                    channel_info.channel_id, i)
                checkbox = QtWidgets.QCheckBox(self)
                checkbox.setText(subchannel)
                spinbox = QtWidgets.QSpinBox(self)
                self.setting_names[setting_name] = (checkbox, spinbox)
                sort_keys[setting_name] = (channel_info.channel_id, i)
                total_channels += 1
        self.modbusChannelCount.setText(str(total_channels))

        # find settings that don't have an existing channel
        for setting_name in self.settings.allKeys():
            if setting_name in self.setting_names:
                continue

            result = pattern.fullmatch(setting_name)
            if result:
                channel_id = int(result.group(1))
                subchannel_id = int(result.group(2))

                checkbox = QtWidgets.QCheckBox(self)
                checkbox.setText("Channel {} Subchannel {}".format(
                    channel_id, subchannel_id))
                spinbox = QtWidgets.QSpinBox(self)
                self.setting_names[setting_name] = (checkbox, spinbox)
                sort_keys[setting_name] = (channel_id, subchannel_id)

        for setting_name in sorted(self.setting_names.keys(),
                                   key=lambda x: sort_keys[x]):
            checkbox, spinbox = self.setting_names[setting_name]
            label = QtWidgets.QLabel("Port:", self)
            checkbox.setChecked(True)  # so the toggled signal will fire
            checkbox.toggled.connect(spinbox.setEnabled)
            checkbox.toggled.connect(label.setEnabled)

            spinbox.setMinimum(1)
            spinbox.setMaximum(65535)

            row = self.gridLayout.rowCount()
            self.gridLayout.addWidget(checkbox, row, 1)
            self.gridLayout.addWidget(label, row, 2)
            self.gridLayout.addWidget(spinbox, row, 3)

    def done(self, r: int) -> None:
        chosen_ports = set()

        for _setting_name, (checkbox, spinbox) in self.setting_names.items():
            if checkbox.isChecked():
                port = spinbox.value()
                if port in chosen_ports:
                    # show a warning
                    m = self.tr('Cannot have duplicate ports!')
                    QtWidgets.QMessageBox.warning(self, self.tr("Error"), m)
                    return
                else:
                    chosen_ports.add(port)
        super().done(r)

    def read_settings(self) -> None:
        self.modbusCheckBox.setChecked(self.device_prefs.modbus_enable)
        self.modbusOffset.setValue(self.device_prefs.modbus_register_offset)

        for setting_name, (checkbox, spinbox) in self.setting_names.items():
            port = read_int_setting(self.settings, setting_name, 0)
            if not port:
                checkbox.setChecked(False)
                spinbox.setValue(12345)
            else:
                checkbox.setChecked(True)
                spinbox.setValue(port)

    @QtCore.Slot()
    def write_settings(self) -> None:
        self.device_prefs.modbus_enable = self.modbusCheckBox.isChecked()
        self.device_prefs.modbus_register_offset = self.modbusOffset.value()

        for setting_name, (checkbox, spinbox) in self.setting_names.items():
            if checkbox.isChecked():
                port = spinbox.value()
                self.settings.setValue(setting_name, port)
            else:
                self.settings.remove(setting_name)

    @QtCore.Slot()
    def show_modbus_details(self) -> None:
        impl = getDOMImplementation()
        if not impl:
            m = self.tr('Error loading serializer!')
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), m)
            logger.error(m)
            return

        dt = impl.createDocumentType(
            "html",
            "-//W3C//DTD XHTML 1.0 Strict//EN",
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd",
        )
        dom = impl.createDocument("http://www.w3.org/1999/xhtml", "html", dt)
        html = dom.documentElement
        head = dom.createElement("head")
        html.appendChild(head)
        title = dom.createElement("title")
        title_string = f"{self.serial_number} Modbus Details"
        title.appendChild(dom.createTextNode(title_string))
        head.appendChild(title)
        body = dom.createElement("body")
        html.appendChild(body)
        h1 = dom.createElement("h1")
        h1.appendChild(dom.createTextNode(title_string))
        body.appendChild(h1)

        # add board name and rev
        p = dom.createElement("p")
        body.appendChild(p)
        board_str = "{} rev {}".format(*self.device_info.board_info)
        p.appendChild(dom.createTextNode(board_str))

        # show the offset
        offset = self.modbusOffset.value()
        p = dom.createElement("p")
        body.appendChild(p)
        b = dom.createElement("b")
        p.appendChild(b)
        b.appendChild(dom.createTextNode(f"Offset: {offset}"))

        # create the table
        table = dom.createElement("table")
        table.setAttribute("border", "1")
        table.setAttribute("cellspacing", "0")
        table.setAttribute("cellpadding", "2")
        body.appendChild(table)

        # create the table header
        top_header_row = dom.createElement("tr")
        table.appendChild(top_header_row)
        bottom_header_row = dom.createElement("tr")
        table.appendChild(bottom_header_row)
        blank_th = dom.createElement("th")
        blank_th.setAttribute("rowspan", "2")
        top_header_row.appendChild(blank_th)

        # populate the table header
        for type_name in ["Mean (1s)", "Std Dev (1s)", "Instant"]:
            top_th = dom.createElement("th")
            top_th.appendChild(dom.createTextNode(type_name))
            top_th.setAttribute("colspan", "2")
            top_header_row.appendChild(top_th)
            float_th = dom.createElement("th")
            float_th.appendChild(dom.createTextNode("Float Registers"))
            bottom_header_row.appendChild(float_th)
            sixteen_bit_th = dom.createElement("th")
            sixteen_bit_th.appendChild(dom.createTextNode("16-Bit Register"))
            bottom_header_row.appendChild(sixteen_bit_th)

        float_unit_th = dom.createElement("th")
        float_unit_th.appendChild(dom.createTextNode("Float Units"))
        float_unit_th.setAttribute("rowspan", "2")
        top_header_row.appendChild(float_unit_th)

        sixteen_bit_range_th = dom.createElement("th")
        sixteen_bit_range_th.appendChild(dom.createTextNode("16-bit Range"))
        sixteen_bit_range_th.setAttribute("colspan", "2")
        top_header_row.appendChild(sixteen_bit_range_th)
        mean_and_instant_th = dom.createElement("th")
        mean_and_instant_th.appendChild(dom.createTextNode("Mean & Instant"))
        bottom_header_row.appendChild(mean_and_instant_th)
        std_dev_th = dom.createElement("th")
        std_dev_th.appendChild(dom.createTextNode("Std Dev"))
        bottom_header_row.appendChild(std_dev_th)

        # generate the device rows
        index = 1
        for channel_id in sorted(self.channel_info):
            channel_info = self.channel_info[channel_id]
            unit = channel_info.channel.unit_type
            res = channel_info.channel.resolution
            uf_base = asphodel.nativelib.create_unit_formatter(
                unit, 1.0, 1.0, 1.0)

            min_mean = "0x0000: {}".format(asphodel.format_value_utf8(
                unit, res, channel_info.channel.minimum))
            max_mean = "0xFFFF: {}".format(asphodel.format_value_utf8(
                unit, res, channel_info.channel.maximum))
            min_std = "0x0000: {}".format(asphodel.format_value_utf8(
                unit, 1.0, 0.0))
            std_range = (channel_info.channel.maximum -
                         channel_info.channel.minimum) / 2.0
            max_std = "0xFFFF: {}".format(asphodel.format_value_utf8(
                unit, res, std_range))

            for subchannel_name in channel_info.subchannel_names:
                tr = dom.createElement("tr")
                table.appendChild(tr)
                th = dom.createElement("th")
                th.appendChild(dom.createTextNode(subchannel_name))
                tr.appendChild(th)

                for i in range(3):
                    float_index = (i * 2000) + index + offset
                    sixteen_bit_index = 1000 + (i * 2000) + index + offset

                    float_td = dom.createElement("td")
                    float_td.appendChild(dom.createTextNode(
                        "{}-{}".format(float_index, float_index + 1)))
                    tr.appendChild(float_td)
                    sixteen_bit_td = dom.createElement("td")
                    sixteen_bit_td.appendChild(dom.createTextNode(
                        f"{sixteen_bit_index}"))
                    tr.appendChild(sixteen_bit_td)

                float_unit_td = dom.createElement("td")
                float_unit_td.appendChild(dom.createTextNode(
                    uf_base.unit_utf8))
                tr.appendChild(float_unit_td)

                mean_range_td = dom.createElement("td")
                mean_range_td.appendChild(dom.createTextNode(min_mean))
                mean_range_td.appendChild(dom.createElement("br"))
                mean_range_td.appendChild(dom.createTextNode(max_mean))
                tr.appendChild(mean_range_td)

                std_range_td = dom.createElement("td")
                std_range_td.appendChild(dom.createTextNode(min_std))
                std_range_td.appendChild(dom.createElement("br"))
                std_range_td.appendChild(dom.createTextNode(max_std))
                tr.appendChild(std_range_td)

                index += 2

        # add a blank paragraph for spacing
        p = dom.createElement("p")
        body.appendChild(p)

        # create the serial number table
        sn_table = dom.createElement("table")
        sn_table.setAttribute("border", "1")
        sn_table.setAttribute("cellspacing", "0")
        sn_table.setAttribute("cellpadding", "2")
        body.appendChild(sn_table)

        # create the serial number table header
        sn_header_row = dom.createElement("tr")
        sn_table.appendChild(sn_header_row)
        blank_th = dom.createElement("th")
        sn_header_row.appendChild(blank_th)
        thirtytwo_bit_th = dom.createElement("th")
        thirtytwo_bit_th.appendChild(dom.createTextNode("32-Bit Register"))
        sn_header_row.appendChild(thirtytwo_bit_th)

        # create the serial number row
        tr = dom.createElement("tr")
        sn_table.appendChild(tr)
        th = dom.createElement("th")
        th.appendChild(dom.createTextNode(
            f"Serial Number ({self.numeric_serial_number})"))
        tr.appendChild(th)
        reg_td = dom.createElement("td")
        reg_td.appendChild(dom.createTextNode(
            "{}-{}".format(6001 + offset, 6002 + offset)))
        tr.appendChild(reg_td)

        # create the channel length row
        tr = dom.createElement("tr")
        sn_table.appendChild(tr)
        th = dom.createElement("th")
        th.appendChild(dom.createTextNode(
            f"Number of Channels ({(index - 1) // 2})"))
        tr.appendChild(th)
        reg_td = dom.createElement("td")
        reg_td.appendChild(dom.createTextNode(
            "{}-{}".format(6003 + offset, 6004 + offset)))
        tr.appendChild(reg_td)

        p = dom.createElement("p")
        body.appendChild(p)
        p.appendChild(dom.createTextNode(
            "Modbus registers are referenced starting at 1."))

        p = dom.createElement("p")
        body.appendChild(p)
        p.appendChild(dom.createTextNode(
            "Values are available in both input registers (3xxxx) and holding "
            "registers (4xxxx). Holding registers are read only."))

        p = dom.createElement("p")
        body.appendChild(p)
        p.appendChild(dom.createTextNode(
            "The float and 32-bit values are stored in two consecutive "
            "registers, least significant register first (LSRF), also known "
            "as ABCD format."))

        outdir = QtCore.QStandardPaths.writableLocation(
            QtCore.QStandardPaths.StandardLocation.AppLocalDataLocation)
        outfile = os.path.join(outdir, f"{self.serial_number}_Modbus.html")

        try:
            with open(outfile, "wb") as f:
                f.write(dom.toxml(encoding="UTF-8"))
        except Exception:
            m = self.tr('Error creating file!')
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), m)
            logger.exception(m)
            return

        url = QtCore.QUrl.fromLocalFile(outfile)
        QtGui.QDesktopServices.openUrl(url)
