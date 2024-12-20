import logging
from typing import Callable, Optional

from PySide6 import QtCore, QtWidgets

from ..core.update_func_limiter import UpdateFuncLimiter
from .ui.ui_rgb_control_widget import Ui_RGBControlWidget

logger = logging.getLogger(__name__)


class RGBControlWidget(Ui_RGBControlWidget, QtWidgets.QWidget):
    def __init__(self, set_rgb: Callable[[tuple[int, int, int]], None],
                 initial_values: tuple[int, int, int],
                 parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        self.setting_color = False

        self.updater = UpdateFuncLimiter(set_rgb, 100, self)

        self.setupUi(self)  # type: ignore

        self.setup_callbacks()

        self.set_values(initial_values)

    def setup_callbacks(self) -> None:
        self.buttons: dict[tuple[int, int, int], QtWidgets.QPushButton] = {
            (255, 255, 255): self.whiteButton,
            (255, 0, 0): self.redButton,
            (0, 255, 0): self.greenButton,
            (0, 0, 255): self.blueButton,
            (0, 255, 255): self.cyanButton,
            (255, 0, 255): self.magentaButton,
            (255, 255, 0): self.yellowButton,
            (0, 0, 0): self.blackButton,
        }

        self.whiteButton.clicked.connect(self.white_button_pressed)
        self.redButton.clicked.connect(self.red_button_pressed)
        self.greenButton.clicked.connect(self.green_button_pressed)
        self.blueButton.clicked.connect(self.blue_button_pressed)
        self.cyanButton.clicked.connect(self.cyan_button_pressed)
        self.magentaButton.clicked.connect(self.magenta_button_pressed)
        self.yellowButton.clicked.connect(self.yellow_button_pressed)
        self.blackButton.clicked.connect(self.black_button_pressed)

        self.redSlider.valueChanged.connect(self.color_changed)
        self.greenSlider.valueChanged.connect(self.color_changed)
        self.blueSlider.valueChanged.connect(self.color_changed)

    @QtCore.Slot()
    def white_button_pressed(self) -> None:
        self.set_color_from_button((255, 255, 255))

    @QtCore.Slot()
    def red_button_pressed(self) -> None:
        self.set_color_from_button((255, 0, 0))

    @QtCore.Slot()
    def green_button_pressed(self) -> None:
        self.set_color_from_button((0, 255, 0))

    @QtCore.Slot()
    def blue_button_pressed(self) -> None:
        self.set_color_from_button((0, 0, 255))

    @QtCore.Slot()
    def cyan_button_pressed(self) -> None:
        self.set_color_from_button((0, 255, 255))

    @QtCore.Slot()
    def magenta_button_pressed(self) -> None:
        self.set_color_from_button((255, 0, 255))

    @QtCore.Slot()
    def yellow_button_pressed(self) -> None:
        self.set_color_from_button((255, 255, 0))

    @QtCore.Slot()
    def black_button_pressed(self) -> None:
        self.set_color_from_button((0, 0, 0))

    def set_values(self, values: tuple[int, int, int]) -> None:
        self.setting_color = True

        self.redSlider.setValue(values[0])
        self.greenSlider.setValue(values[1])
        self.blueSlider.setValue(values[2])

        for color, button in self.buttons.items():
            checked = (color == tuple(values))
            button.setDown(checked)

        self.setting_color = False

    def set_color_from_button(self, values: tuple[int, int, int]) -> None:
        self.set_values(values)
        self.updater.update(values)

    @QtCore.Slot()
    def color_changed(self) -> None:
        if not self.setting_color:
            values = (self.redSlider.value(), self.greenSlider.value(),
                      self.blueSlider.value())
            self.set_values(values)
            self.updater.update(values)
