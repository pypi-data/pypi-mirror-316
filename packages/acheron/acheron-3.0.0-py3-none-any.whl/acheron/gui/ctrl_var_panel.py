import logging
from typing import Optional

from PySide6 import QtWidgets

from .ui.ui_ctrl_var_panel import Ui_CtrlVarPanel

logger = logging.getLogger(__name__)


class CtrlVarPanel(Ui_CtrlVarPanel, QtWidgets.QGroupBox):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.setupUi(self)  # type: ignore

    def add_ctrl_var_widget(self, widget: QtWidgets.QWidget) -> None:
        self.ctrlVarLayout.addWidget(widget)

    def clear_ctrl_var_widgets(self) -> None:
        while True:
            item = self.ctrlVarLayout.takeAt(0)
            if not item:
                break
            # NOTE: the items are deleted by the caller
