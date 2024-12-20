from dataclasses import dataclass
import functools
import logging
import math
import platform
from typing import Any, Callable, cast, Optional, TYPE_CHECKING
import weakref
from weakref import ReferenceType

import numpy
from numpy.typing import NDArray
import pyqtgraph
from PySide6 import QtCore, QtWidgets

import asphodel
from asphodel.device_info import DeviceInfo
from hyperborea.unit_formatter_spinbox import UnitFormatterDoubleSpinBox
from hyperborea.unit_selection_dialog import UnitSelectionDialog

from ..device_logging import DeviceLoggerAdapter
from ..core.calibration import get_channel_setting_values, update_nvm
from ..connectivity.event_upload import EventUploader
from .ui.ui_calibration_panel import Ui_CalibrationPanel
from .ui.ui_calibration_channel import Ui_CalibrationChannel

if TYPE_CHECKING:
    from .device_tab import DeviceTab

logger = logging.getLogger(__name__)


@dataclass
class CalibrationConnection:
    name: str
    calibration_info: asphodel.ChannelCalibration
    channel_id: int
    device_tab: "ReferenceType[DeviceTab]"
    unit_formatter: asphodel.AsphodelNativeUnitFormatter


class CalibrationChannel(Ui_CalibrationChannel, QtWidgets.QWidget):
    value_changed = QtCore.Signal()

    def __init__(self, cal: CalibrationConnection,
                 unit_selection_dialog: UnitSelectionDialog,
                 cal_panel: "CalibrationPanel"):
        super().__init__(cal_panel)

        self.cal = cal
        self.unit_selection_dialog = unit_selection_dialog

        # create unit formatters for the capture side with 0 resolution
        unit_formatter = cal.unit_formatter
        self.rms_formatter = asphodel.nativelib.create_custom_unit_formatter(
            unit_formatter.conversion_scale, 0.0,
            0.0, unit_formatter.unit_ascii, unit_formatter.unit_utf8,
            unit_formatter.unit_html)
        self.dc_formatter = asphodel.nativelib.create_custom_unit_formatter(
            unit_formatter.conversion_scale, unit_formatter.conversion_offset,
            0.0, unit_formatter.unit_ascii, unit_formatter.unit_utf8,
            unit_formatter.unit_html)

        self.unit_info: Optional[
            tuple[int, asphodel.AsphodelNativeUnitFormatter]] = None
        self.scale_offset: Optional[tuple[float, float]] = None

        self.linear_x: NDArray[numpy.float64] = numpy.zeros(0)
        self.linear_y: NDArray[numpy.float64] = numpy.zeros(0)

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup()
        self.setup_plot()

        # process the current state
        self.update_all()

    def extra_ui_setup(self) -> None:
        self.calibrationEnabled.toggled.connect(self.update_all)

        # this is easily forgotten in Qt Designer
        self.tabWidget.setCurrentIndex(0)

        self.tabWidget.currentChanged.connect(self.update_all)

        self.selectUnit.clicked.connect(self.select_unit)

        self.unit.setText("")

        self.acCapture.clicked.connect(self.ac_capture)
        self.linearCapture.clicked.connect(self.linear_capture)

        self.plotButton.clicked.connect(self.plot_linear)

        self.capturedMagnitude.set_unit_formatter(self.rms_formatter)
        self.capturedOffset.set_unit_formatter(self.dc_formatter)

        self.capturedMagnitude.setMinimum(-math.inf)
        self.capturedMagnitude.setMaximum(math.inf)
        self.capturedOffset.setMinimum(-math.inf)
        self.capturedOffset.setMaximum(math.inf)
        self.actualMagnitude.setMinimum(-math.inf)
        self.actualMagnitude.setMaximum(math.inf)
        self.actualOffset.setMinimum(-math.inf)
        self.actualOffset.setMaximum(math.inf)

        self.capturedMagnitude.valueChanged.connect(self.update_scale_offset)
        self.capturedOffset.valueChanged.connect(self.update_scale_offset)
        self.actualMagnitude.valueChanged.connect(self.update_scale_offset)
        self.actualOffset.valueChanged.connect(self.update_scale_offset)

        header = self.linearTable.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

    def setup_plot(self) -> None:

        self.plot: pyqtgraph.PlotItem = cast(pyqtgraph.PlotItem,
                                             self.graphicsView.getPlotItem())

        self.plot.showGrid(x=True, y=True)
        self.plot.setLabel("bottom", "Time (s)")
        self.plot.setTitle("Linear Fit")

        self.plot.setLabel("bottom", self.dc_formatter.unit_html)

        self.points_curve = self.plot.plot(
            pen=None, symbol='o', symbolBrush=(255, 0, 0), symbolPen='w',
            name="Data")
        self.regression_curve = self.plot.plot(pen=(0, 0, 255), name="Fit")

        self.text_items: list[pyqtgraph.TextItem] = []

    @QtCore.Slot()
    def select_unit(self) -> None:
        dialog = self.unit_selection_dialog
        ret = dialog.exec()
        if ret == 0:
            return  # user cancelled

        unit_info = dialog.get_unit_info()
        if not unit_info:
            return

        self.unit_info = unit_info
        unit_formatter = self.unit_info[1]
        self.unit.setText(unit_formatter.unit_utf8)

        rms_formatter = asphodel.nativelib.create_custom_unit_formatter(
            unit_formatter.conversion_scale, 0.0, 0.0,
            unit_formatter.unit_ascii, unit_formatter.unit_utf8,
            unit_formatter.unit_html)

        self.actualMagnitude.set_unit_formatter(rms_formatter)
        self.actualOffset.set_unit_formatter(unit_formatter)

        row_count = self.linearTable.rowCount()
        for row in range(row_count):
            actual = cast(UnitFormatterDoubleSpinBox,
                          self.linearTable.cellWidget(row, 1))
            actual.set_unit_formatter(unit_formatter)

        self.plot.setLabel("left", unit_formatter.unit_html)

        self.update_all()

    def update_enabled(self) -> None:
        enabled = self.calibrationEnabled.isChecked()

        self.unitLabel.setEnabled(enabled)
        self.unit.setEnabled(enabled)
        self.selectUnit.setEnabled(enabled)

        if enabled:
            unit_ready = self.unit_info is not None
        else:
            unit_ready = False
        self.linearPage.setEnabled(unit_ready)
        self.acPage.setEnabled(unit_ready)
        self.scaleLabel.setEnabled(unit_ready)
        self.scale.setEnabled(unit_ready)
        self.offsetLabel.setEnabled(unit_ready)
        self.offset.setEnabled(unit_ready)

    @QtCore.Slot()
    def update_all(self) -> None:
        self.update_enabled()
        self.update_scale_offset()

    def get_ac_scale_offset(self) -> Optional[tuple[float, float]]:
        try:
            unscaled_captured_mag = (self.capturedMagnitude.value() /
                                     self.cal.calibration_info.scale)
            unscaled_captured_offset = ((self.capturedOffset.value() -
                                         self.cal.calibration_info.offset) /
                                        self.cal.calibration_info.scale)

            scale = self.actualMagnitude.value() / unscaled_captured_mag

            if scale == 0:
                # invalid
                return None

            offset = (self.actualOffset.value() -
                      unscaled_captured_offset * scale)
            return (scale, offset)
        except ZeroDivisionError:
            return None

    def get_linear_scale_offset(self) -> Optional[tuple[float, float]]:
        # least squares regression to fit y = m*x + b, where y is the actual
        # values, x is the captured values, m is the scale and b is the offset.
        # numpy.linalg.lstsq requires A matrix to be [[x 1]]
        try:
            row_count = self.linearTable.rowCount()
            if row_count < 2:
                # not enough points
                return None

            x = numpy.zeros(row_count)
            y = numpy.zeros(row_count)

            for row in range(row_count):
                captured = cast(UnitFormatterDoubleSpinBox,
                                self.linearTable.cellWidget(row, 0))
                actual = cast(UnitFormatterDoubleSpinBox,
                              self.linearTable.cellWidget(row, 1))

                unscaled = ((captured.value() -
                             self.cal.calibration_info.offset) /
                            self.cal.calibration_info.scale)

                x[row] = unscaled
                y[row] = actual.value()

            self.linear_x = x
            self.linear_y = y

            A = numpy.vstack([x, numpy.ones(row_count)]).T
            m, b = numpy.linalg.lstsq(A, y, rcond=None)[0]

            if m == 0 or not math.isfinite(m) or not math.isfinite(b):
                # invalid
                return None

            return (m, b)
        except Exception:
            return None

    def update_linear_plot(self) -> None:
        row_count = self.linearTable.rowCount()

        x = numpy.zeros(row_count)
        y = numpy.zeros(row_count)

        for row in range(row_count):
            captured = cast(UnitFormatterDoubleSpinBox,
                            self.linearTable.cellWidget(row, 0))
            actual = cast(UnitFormatterDoubleSpinBox,
                          self.linearTable.cellWidget(row, 1))

            x[row] = captured.value()
            y[row] = actual.value()

        # apply the unit formatters
        x = ((x * self.dc_formatter.conversion_scale) +
             self.dc_formatter.conversion_offset)
        if self.unit_info:
            actual_unit_formatter = self.unit_info[1]
            y = ((y * actual_unit_formatter.conversion_scale) +
                 actual_unit_formatter.conversion_offset)

        # clear out any old text items
        for text_item in self.text_items:
            self.plot.removeItem(text_item)
        self.text_items.clear()

        # update the plot
        self.points_curve.setData(x, y)

        # add new text items
        for i, (x_point, y_point) in enumerate(zip(x, y)):
            text_item = pyqtgraph.TextItem(
                "{}".format(i + 1), anchor=(0.5, 1.1))
            text_item.setPos(x_point, y_point)
            self.text_items.append(text_item)
            self.plot.addItem(text_item)

        if len(x) < 2:
            self.regression_curve.clear()
        else:
            # do least squares
            A = numpy.vstack([x, numpy.ones(row_count)]).T
            scale, offset = numpy.linalg.lstsq(A, y, rcond=None)[0]

            x_linear = numpy.array([x.min(), x.max()])
            y_linear = x_linear * scale + offset

            self.regression_curve.setData(x_linear, y_linear)

    @QtCore.Slot()
    def update_scale_offset(self) -> None:
        if self.unit_info is None:
            self.scale_offset = None
        elif self.tabWidget.currentIndex() == 0:
            self.scale_offset = self.get_linear_scale_offset()
            self.update_linear_plot()
        else:
            self.scale_offset = self.get_ac_scale_offset()

        if self.scale_offset is None:
            self.scale.setText("")
            self.offset.setText("")
            self.plotButton.setEnabled(False)
        else:
            scale, offset = self.scale_offset
            self.scale.setText(str(scale))
            self.offset.setText(str(offset))
            self.plotButton.setEnabled(True)

        self.value_changed.emit()

    def get_results(self) -> Optional[tuple[int, float, float,
                                            dict[str, Any]]]:
        if self.unit_info is None:
            return None
        unit_type, unit_formatter = self.unit_info

        if self.scale_offset is None:
            return None
        scale, offset = self.scale_offset

        try:
            unit_type_str = asphodel.unit_type_names[unit_type]
        except IndexError:
            unit_type_str = str(unit_type)

        base_event_data = {
            "calibration_unit": unit_formatter.unit_utf8,
            "output_unit": unit_type_str,
            "scale": scale,
            "offset": offset,
        }

        if self.tabWidget.currentIndex() == 0:
            base_event_data["calibration_type"] = "Linear"
            base_event_data["x"] = list(self.linear_x)
            base_event_data["y"] = list(self.linear_y)
        else:
            base_event_data["calibration_type"] = "AC RMS"

        channel_suffix = f"_Ch{self.cal.channel_id}_{self.cal.name}"

        event_data = {(k + channel_suffix): v for k, v in
                      base_event_data.items()}

        return (unit_type, scale, offset, event_data)

    @QtCore.Slot()
    def ac_capture(self) -> None:
        device_tab = self.cal.device_tab()
        if device_tab is None:
            return

        mean, std_dev = device_tab.capture_func(self.cal.channel_id)
        mean_value = mean.item()
        std_dev_value = std_dev.item()

        if math.isfinite(mean_value) and math.isfinite(std_dev_value):
            self.capturedMagnitude.setValue(std_dev_value)
            self.capturedOffset.setValue(mean_value)
            self.update_scale_offset()

    @QtCore.Slot()
    def linear_capture(self) -> None:
        if self.unit_info is None:
            return

        device_tab = self.cal.device_tab()
        if device_tab is None:
            return

        mean, std_dev = device_tab.capture_func(self.cal.channel_id)
        mean_value = mean.item()
        std_dev_value = std_dev.item()

        if math.isfinite(mean_value) and math.isfinite(std_dev_value):
            captured = UnitFormatterDoubleSpinBox(self)
            captured.set_unit_formatter(self.dc_formatter)
            captured.setMinimum(-math.inf)
            captured.setMaximum(math.inf)
            captured.setValue(mean_value)
            captured.valueChanged.connect(self.update_scale_offset)

            actual = UnitFormatterDoubleSpinBox(self)
            actual.set_unit_formatter(self.unit_info[1])
            actual.setMinimum(-math.inf)
            actual.setMaximum(math.inf)
            actual.setValue(0.0)
            actual.valueChanged.connect(self.update_scale_offset)

            delete = QtWidgets.QPushButton(self.tr("Delete"))

            # use a weakref in the partial to allow GC
            delete.clicked.connect(
                functools.partial(self.delete_cb, weakref.ref(delete)))

            row = self.linearTable.rowCount()
            self.linearTable.insertRow(row)
            self.linearTable.setCellWidget(row, 0, captured)
            self.linearTable.setCellWidget(row, 1, actual)
            self.linearTable.setCellWidget(row, 2, delete)

            # give it focus
            actual.setFocus()
            actual.selectAll()

            self.update_scale_offset()

    @QtCore.Slot()
    def plot_linear(self) -> None:
        if self.scale_offset is None or self.unit_info is None:
            return

        row_count = self.linearTable.rowCount()
        if row_count < 2:
            # not enough points
            return

        y = numpy.zeros(row_count)
        x = numpy.zeros(row_count)

        for row in range(row_count):
            captured = cast(UnitFormatterDoubleSpinBox,
                            self.linearTable.cellWidget(row, 0))
            actual = cast(UnitFormatterDoubleSpinBox,
                          self.linearTable.cellWidget(row, 1))

            y[row] = actual.value()
            x[row] = captured.value()

        # apply the unit formatters
        x = ((x * self.dc_formatter.conversion_scale) +
             self.dc_formatter.conversion_offset)
        actual_unit_formatter = self.unit_info[1]
        y = ((y * actual_unit_formatter.conversion_scale) +
             actual_unit_formatter.conversion_offset)

        # do least squares
        A = numpy.vstack([x, numpy.ones(row_count)]).T
        scale, offset = numpy.linalg.lstsq(A, y, rcond=None)[0]

        # create line
        x_linear = numpy.array([x.min(), x.max()])
        y_linear = x_linear * scale + offset

        dialog = QtWidgets.QDialog(self)
        dialog.resize(500, 500)
        layout = QtWidgets.QVBoxLayout(dialog)
        graphics_layout = pyqtgraph.GraphicsLayoutWidget(dialog)
        layout.addWidget(graphics_layout)
        button_box = QtWidgets.QDialogButtonBox(dialog)
        button_box.setOrientation(QtCore.Qt.Orientation.Horizontal)
        button_box.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Close)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        plot = graphics_layout.addPlot(title="Linear Fit")  # type: ignore
        plot.plot(x, y, pen=None, symbol='o', symbolBrush=(255, 0, 0),
                  symbolPen='w', name="Data")
        plot.plot(x_linear, y_linear, pen=(0, 0, 255), name="Fit")

        for row in range(row_count):
            text_item = pyqtgraph.TextItem(f"{row + 1}", anchor=(0.5, 1.1))
            text_item.setPos(x[row], y[row])
            plot.addItem(text_item)

        plot.setLabel("left", actual_unit_formatter.unit_html)
        plot.setLabel("bottom", self.dc_formatter.unit_html)

        dialog.exec()

    def delete_cb(self, ref: "ReferenceType[QtWidgets.QPushButton]") -> None:
        button = ref()
        if button is None:
            return

        row_count = self.linearTable.rowCount()
        for row in range(row_count):
            widget = self.linearTable.cellWidget(row, 2)
            if widget == button:
                self.linearTable.removeRow(row)
                self.linearTable.clearSelection()
                self.update_scale_offset()
                return


class CalibrationPanel(Ui_CalibrationPanel, QtWidgets.QGroupBox):
    def __init__(self, device_info: DeviceInfo,
                 cals: list[CalibrationConnection],
                 logger: DeviceLoggerAdapter,
                 write_nvm: Callable[[bytearray], None],
                 event_uploader: EventUploader,
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.device_info = device_info
        self.cals = cals
        self.logger = logger
        self.write_nvm = write_nvm
        self.event_uploader = event_uploader

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup()

    def extra_ui_setup(self) -> None:
        self.unit_selection_dialog = UnitSelectionDialog(self)

        self.saveButton = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.saveButton.setText(self.tr("Write NVM"))
        self.saveButton.clicked.connect(self.save)

        self.channel_widgets: list[tuple[str, CalibrationChannel]] = []

        for cal in self.cals:
            channel_widget = CalibrationChannel(
                cal, self.unit_selection_dialog, self)
            self.channel_widgets.append((cal.name, channel_widget))
            self.setup_channel_signals(channel_widget)

        if len(self.channel_widgets) == 1:
            channel_widget = self.channel_widgets[0][1]
            channel_widget.calibrationEnabled.setChecked(True)
            channel_widget.calibrationEnabled.setVisible(False)
            self.verticalLayout.insertWidget(0, channel_widget)
        elif len(self.channel_widgets) > 1:
            self.tabWidget = QtWidgets.QTabWidget(self)
            self.verticalLayout.insertWidget(0, self.tabWidget)
            for name, channel_widget in self.channel_widgets:
                channel_widget.calibrationEnabled.setChecked(False)
                cal_str = self.tr("Calibrate {}").format(name)
                channel_widget.calibrationEnabled.setText(cal_str)
                self.tabWidget.addTab(channel_widget, name)

    def setup_channel_signals(
            self, channel_widget: CalibrationChannel) -> None:
        channel_widget.value_changed.connect(self.values_updated)

    def is_valid(self) -> bool:
        all_valid = False
        for _name, channel_widget in self.channel_widgets:
            if channel_widget.calibrationEnabled.isChecked():
                if channel_widget.get_results() is not None:
                    all_valid = True
                else:
                    return False
        return all_valid

    @QtCore.Slot()
    def values_updated(self) -> None:
        valid = self.is_valid()
        self.saveButton.setEnabled(valid)

    @QtCore.Slot()
    def save(self) -> None:
        settings = self.device_info.settings

        unit_settings: dict[int, int] = {}
        float_settings: dict[int, float] = {}

        event_data = {
            "board_type": self.device_info.board_info[0],
            "board_rev": self.device_info.board_info[1],
            "computer": platform.node(),
        }

        for _name, channel_widget in self.channel_widgets:
            if channel_widget.calibrationEnabled.isChecked():
                results = channel_widget.get_results()
                if results:
                    unit_type, scale, offset, channel_event_data = results
                    u, f = get_channel_setting_values(
                        len(settings), channel_widget.cal.calibration_info,
                        unit_type, scale, offset)
                    unit_settings.update(u)
                    float_settings.update(f)
                    event_data.update(channel_event_data)

        new_nvm = update_nvm(
            self.device_info.nvm, settings,
            unit_settings, float_settings, self.logger)

        self.event_uploader.calibration_finished(
            self.device_info.serial_number, event_data)

        self.write_nvm(new_nvm)
