import logging
from typing import Any, Optional

from PySide6 import QtCore, QtWidgets

from .ui.ui_download_firmware_dialog import Ui_DownloadFirmwareDialog

logger = logging.getLogger(__name__)


class DownloadFirmwareDialog(Ui_DownloadFirmwareDialog, QtWidgets.QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup()

    def extra_ui_setup(self) -> None:
        self.board_button_group = QtWidgets.QButtonGroup(self)
        self.board_button_group.addButton(self.boardRadioButton)
        self.board_button_group.addButton(self.repoRadioButton)

        self.board_button_group = QtWidgets.QButtonGroup(self)
        self.board_button_group.addButton(self.branchRadioButton)
        self.board_button_group.addButton(self.commitRadioButton)

        self.boardRadioButton.setChecked(True)
        self.branchRadioButton.setChecked(True)

        self.boardRadioButton.toggled.connect(self.values_updated)
        self.repoRadioButton.toggled.connect(self.values_updated)
        self.branchRadioButton.toggled.connect(self.values_updated)
        self.commitRadioButton.toggled.connect(self.values_updated)
        self.boardName.textEdited.connect(self.values_updated)
        self.repoName.textEdited.connect(self.values_updated)
        self.branchName.textEdited.connect(self.values_updated)
        self.commitHash.textEdited.connect(self.values_updated)

        self.values_updated()

    def is_valid(self) -> bool:
        if self.boardRadioButton.isChecked():
            if not self.boardName.text().strip():
                return False
        else:  # self.repoRadioButton.isChecked()
            if not self.repoName.text().strip():
                return False

        if self.branchRadioButton.isChecked():
            if not self.branchName.text().strip():
                return False
        else:  # self.commitRadioButton.isChecked()
            if not self.commitHash.text().strip():
                return False

        return True

    def done(self, r: int) -> None:
        if r and not self.is_valid():
            return
        super().done(r)

    @QtCore.Slot()
    def values_updated(self) -> None:
        ok_button = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Ok)
        if self.is_valid():
            ok_button.setEnabled(True)
        else:
            ok_button.setEnabled(False)

    def get_results(self) -> dict[str, Any]:
        results = {}
        if self.boardRadioButton.isChecked():
            board_name = self.boardName.text().strip()
            board_rev = self.boardRev.value()
            results['board_info'] = (board_name, board_rev)
        else:  # self.repoRadioButton.isChecked()
            results['repo'] = self.repoName.text().strip()

        if self.branchRadioButton.isChecked():
            results['branch'] = self.branchName.text().strip()
        else:  # self.commitRadioButton.isChecked()
            results['commit'] = self.commitHash.text().strip()

        return results
