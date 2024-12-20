import logging
from typing import Callable, Optional

from PySide6 import QtCore, QtWidgets

import asphodel
from hyperborea.unit_formatter_spinbox import UnitFormatterSpinBox

from ..core.update_func_limiter import UpdateFuncLimiter
from .ui.ui_ctrl_var_widget import Ui_CtrlVarWidget

logger = logging.getLogger(__name__)


class CtrlVarWidget(Ui_CtrlVarWidget, QtWidgets.QWidget):
    def __init__(self, set_setting: Callable[[int], None], name: str,
                 ctrl_var_info: asphodel.CtrlVarInfo, initial_value: int,
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.ctrl_var_info = ctrl_var_info
        self.setting_value = False

        self.updater = UpdateFuncLimiter(set_setting, 100, self)

        self.setupUi(self)  # type: ignore
        self.nameLabel.setText(name)

        self.setup_spinbox(initial_value)
        self.setup_callbacks()

        self.set_value(initial_value)

    def setup_spinbox(self, initial_value: int) -> None:
        scaled_min = (self.ctrl_var_info.minimum * self.ctrl_var_info.scale +
                      self.ctrl_var_info.offset)
        scaled_max = (self.ctrl_var_info.maximum * self.ctrl_var_info.scale +
                      self.ctrl_var_info.offset)
        unit_formatter = asphodel.nativelib.create_unit_formatter(
            self.ctrl_var_info.unit_type, scaled_min, scaled_max,
            self.ctrl_var_info.scale)

        # update the unit formatter's scale and offset with the ctrl var's
        unit_formatter.conversion_offset += (self.ctrl_var_info.offset *
                                             unit_formatter.conversion_scale)
        unit_formatter.conversion_scale *= self.ctrl_var_info.scale

        if unit_formatter.conversion_scale < 0.0:
            self.inverted = True
            unit_formatter.conversion_scale = -unit_formatter.conversion_scale
        else:
            self.inverted = False

        self.spinBox = UnitFormatterSpinBox(self)
        self.spinBox.set_unit_formatter(unit_formatter)
        self.horizontalLayout.addWidget(self.spinBox)

        if not self.inverted:
            minimum = self.ctrl_var_info.minimum
            maximum = self.ctrl_var_info.maximum
            value = initial_value
        else:
            minimum = -self.ctrl_var_info.maximum
            maximum = -self.ctrl_var_info.minimum
            value = -initial_value

        self.spinBox.setMinimum(minimum)
        self.spinBox.setMaximum(maximum)
        self.spinBox.setValue(value)
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.slider.setValue(value)

        self.spinBox.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.spinBox.setValue)

    def setup_callbacks(self) -> None:
        self.slider.valueChanged.connect(self.value_changed)

    def set_value(self, value: int) -> None:
        self.setting_value = True
        if not self.inverted:
            self.slider.setValue(value)
        else:
            self.slider.setValue(-value)
        self.setting_value = False

    @QtCore.Slot()
    def value_changed(self) -> None:
        if not self.setting_value:
            value = self.slider.value()
            if self.inverted:
                value = -value
            self.updater.update(value)
