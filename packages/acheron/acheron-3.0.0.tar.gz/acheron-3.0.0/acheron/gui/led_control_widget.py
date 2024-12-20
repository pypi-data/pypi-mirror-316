import logging
from typing import Callable, Optional

from PySide6 import QtCore, QtWidgets

from ..core.update_func_limiter import UpdateFuncLimiter
from .ui.ui_led_control_widget import Ui_LEDControlWidget

logger = logging.getLogger(__name__)


class LEDControlWidget(Ui_LEDControlWidget, QtWidgets.QWidget):
    def __init__(self, set_led: Callable[[int], None], initial_value: int,
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.setting_value = False

        self.updater = UpdateFuncLimiter(set_led, 100, self)

        self.setupUi(self)  # type: ignore

        self.setup_callbacks()

        self.set_value(initial_value)

    def setup_callbacks(self) -> None:
        self.slider.valueChanged.connect(self.value_changed)

    def set_value(self, value: int) -> None:
        self.setting_value = True
        self.slider.setValue(value)
        self.setting_value = False

    @QtCore.Slot()
    def value_changed(self) -> None:
        if not self.setting_value:
            value = self.slider.value()
            self.updater.update(value)
