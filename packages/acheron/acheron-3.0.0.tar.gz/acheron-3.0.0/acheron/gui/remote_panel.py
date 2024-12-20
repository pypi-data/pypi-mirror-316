from __future__ import annotations
import logging

from PySide6 import QtCore, QtWidgets

from .ui.ui_remote_panel import Ui_RemotePanel

logger = logging.getLogger(__name__)


class RemotePanel(Ui_RemotePanel, QtWidgets.QGroupBox):
    show_radio_clicked = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.setupUi(self)  # type: ignore

        self.goToParentButton.clicked.connect(self.show_radio_clicked)
