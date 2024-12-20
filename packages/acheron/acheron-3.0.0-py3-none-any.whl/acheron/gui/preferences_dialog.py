import logging

from PySide6 import QtCore, QtWidgets

from hyperborea.dark_mode import set_style

from ..core.preferences import Preferences
from ..connectivity.alert_emailer import EmailSettings, send_test_email
from .ui.ui_preferences_dialog import Ui_PreferencesDialog

logger = logging.getLogger(__name__)


class PreferencesDialog(Ui_PreferencesDialog, QtWidgets.QDialog):
    def __init__(self, preferences: Preferences, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.preferences = preferences

        self.setupUi(self)  # type: ignore

        # this is easily forgotten in Qt Designer
        self.tabWidget.setCurrentIndex(0)

        self.accepted.connect(self.write_settings)
        self.rejected.connect(self.restore_dark_mode)
        self.browseButton.clicked.connect(self.browse_cb)
        self.testEmail.clicked.connect(self.test_email_cb)

        self.read_settings()

        self.darkMode.toggled.connect(self.dark_mode_updated)
        self.lightMode.toggled.connect(self.dark_mode_updated)

    @QtCore.Slot()
    def browse_cb(self) -> None:
        base_dir = self.outputLocation.text()
        base_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, dir=base_dir)

        if base_dir:
            self.outputLocation.setText(base_dir)

    @QtCore.Slot()
    def test_email_cb(self) -> None:
        if self.useSTARTTLS.isChecked():
            security = 'starttls'
        elif self.useSSL.isChecked():
            security = 'ssl'
        else:
            security = ''

        email_settings = EmailSettings(
            from_address=self.fromAddress.text().strip(),
            to_address=self.toAddress.text().strip(),
            smtp_host=self.smtpHost.text().strip(),
            smtp_port=self.smtpPort.value(),
            security=security,
            use_auth=self.useAuthentication.isChecked(),
            smtp_user=self.smtpUser.text().strip(),
            smtp_password=self.smtpPassword.text().strip(),
        )

        try:
            QtWidgets.QApplication.setOverrideCursor(
                QtCore.Qt.CursorShape.WaitCursor)
            send_test_email(email_settings)
            QtWidgets.QApplication.restoreOverrideCursor()
            logger.info("Sent test email successfully")
            QtWidgets.QMessageBox.information(self, self.tr("Sent"),
                                              self.tr("Email Sent!"))
        except Exception as e:
            QtWidgets.QApplication.restoreOverrideCursor()
            logger.exception("Error sending test email.")
            error_str = str(e) + "\nSee log for more details."
            QtWidgets.QMessageBox.critical(self, self.tr("Error"), error_str)

    @QtCore.Slot()
    def dark_mode_updated(self) -> None:
        dark_mode = self.darkMode.isChecked()
        set_style(QtWidgets.QApplication.instance(), dark_mode)  # type: ignore

    @QtCore.Slot()
    def restore_dark_mode(self) -> None:
        set_style(QtWidgets.QApplication.instance(),  # type: ignore
                  self.preferences.dark_mode)

    def read_settings(self) -> None:
        self.darkMode.setChecked(self.preferences.dark_mode)
        self.showSupplyChecks.setChecked(self.preferences.show_supplies)

        self.automaticRGBCheckBox.setChecked(self.preferences.auto_rgb)
        self.downsampleCheckBox.setChecked(self.preferences.downsample)
        self.plotMeanCheckBox.setChecked(self.preferences.plot_mean)

        self.unitPreferences.read_settings()

        self.outputLocation.setText(self.preferences.base_dir)
        self.outputLocation.setCursorPosition(0)
        self.compressionLevel.setValue(self.preferences.compression_level)
        self.runModbusCheckBox.setChecked(self.preferences.modbus_enable)
        self.modbusPort.setValue(self.preferences.modbus_port)

        self.enableUpload.setChecked(self.preferences.upload_enabled)
        self.s3Bucket.setText(self.preferences.s3_bucket)
        self.awsRegion.setText(self.preferences.aws_region)
        self.uploadDirectory.setText(self.preferences.upload_directory)
        self.uploadAccessKeyID.setText(self.preferences.access_key_id)
        self.uploadSecretAccessKey.setText(self.preferences.secret_access_key)
        self.uploadDeleteOriginal.setChecked(self.preferences.delete_original)

        self.eventUploadEnabled.setChecked(
            self.preferences.event_upload_enabled)

        self.enableAlertEmail.setChecked(self.preferences.alert_email_enabled)
        self.fromAddress.setText(self.preferences.alert_from_address)
        self.toAddress.setText(self.preferences.alert_to_address)
        self.smtpHost.setText(self.preferences.alert_smtp_host)
        self.smtpPort.setValue(self.preferences.alert_smtp_port)

        security = self.preferences.alert_security.lower()
        if security == "starttls":
            self.useSTARTTLS.setChecked(True)
        elif security == "ssl":
            self.useSSL.setChecked(True)
        elif security == "":
            self.noSecurity.setChecked(True)
        else:
            self.useSTARTTLS.setChecked(True)  # default

        self.useAuthentication.setChecked(self.preferences.alert_use_auth)
        self.smtpUser.setText(self.preferences.alert_smtp_user)
        self.smtpPassword.setText(self.preferences.alert_smtp_password)

    @QtCore.Slot()
    def write_settings(self) -> None:
        self.preferences.dark_mode = self.darkMode.isChecked()
        self.preferences.show_supplies = self.showSupplyChecks.isChecked()

        self.preferences.auto_rgb = self.automaticRGBCheckBox.isChecked()
        self.preferences.downsample = self.downsampleCheckBox.isChecked()
        self.preferences.plot_mean = self.plotMeanCheckBox.isChecked()

        self.unitPreferences.write_settings()

        self.preferences.base_dir = self.outputLocation.text()
        self.preferences.compression_level = self.compressionLevel.value()
        self.preferences.modbus_enable = self.runModbusCheckBox.isChecked()
        self.preferences.modbus_port = self.modbusPort.value()

        self.preferences.upload_enabled = self.enableUpload.isChecked()
        self.preferences.s3_bucket = self.s3Bucket.text()
        self.preferences.aws_region = self.awsRegion.text()
        self.preferences.upload_directory = self.uploadDirectory.text()
        self.preferences.access_key_id = self.uploadAccessKeyID.text()
        self.preferences.secret_access_key = self.uploadSecretAccessKey.text()
        self.preferences.delete_original = \
            self.uploadDeleteOriginal.isChecked()

        self.preferences.event_upload_enabled = \
            self.eventUploadEnabled.isChecked()

        self.preferences.alert_email_enabled = \
            self.enableAlertEmail.isChecked()
        self.preferences.alert_from_address = self.fromAddress.text()
        self.preferences.alert_to_address = self.toAddress.text()
        self.preferences.alert_smtp_host = self.smtpHost.text()
        self.preferences.alert_smtp_port = self.smtpPort.value()
        if self.useSTARTTLS.isChecked():
            self.preferences.alert_security = "starttls"
        elif self.useSSL.isChecked():
            self.preferences.alert_security = "ssl"
        else:
            self.preferences.alert_security = ""
        use_auth = self.useAuthentication.isChecked()
        self.preferences.alert_use_auth = use_auth
        if use_auth:
            self.preferences.alert_smtp_user = self.smtpUser.text()
            self.preferences.alert_smtp_password = self.smtpPassword.text()
        else:
            self.preferences.alert_smtp_user = ""
            self.preferences.alert_smtp_password = ""
