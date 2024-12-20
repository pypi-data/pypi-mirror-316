import logging
from typing import Any, Optional

from PySide6 import QtCore, QtWidgets

from .ui.ui_tcp_connect_dialog import Ui_TCPConnectDialog

logger = logging.getLogger(__name__)


class TCPConnectDialog(Ui_TCPConnectDialog, QtWidgets.QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        self.settings = QtCore.QSettings()

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup()

    def extra_ui_setup(self) -> None:
        # load initial values from settings
        hostname = self.settings.value("connectHostname")
        if hostname and isinstance(hostname, str):
            self.hostname.setText(hostname.strip())

        port = self.settings.value("connectPort")
        if port is not None:
            try:
                port = int(port)  # type: ignore
                self.port.setValue(port)
            except ValueError:
                pass

        serial = self.settings.value("connectSerial")
        if serial and isinstance(serial, str):
            self.serial.setText(serial.strip())

        self.hostname.textEdited.connect(self.values_updated)

        self.values_updated()

    def is_valid(self) -> bool:
        if not self.hostname.text().strip():
            return False

        return True

    def done(self, r: int) -> None:
        if r and not self.is_valid():
            return

        # save settings
        self.settings.setValue("connectHostname", self.hostname.text().strip())
        self.settings.setValue("connectPort", self.port.value())
        self.settings.setValue("connectSerial", self.serial.text().strip())

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
        results = {'hostname': self.hostname.text().strip(),
                   'port': self.port.value()}

        sn = self.serial.text().strip()
        if len(sn) != 0:
            results['serial_number'] = sn
        else:
            results['serial_number'] = None

        return results
