import logging

from PySide6 import QtCore, QtWidgets

from ..core.device_controller import DeviceController, RFPowerStatus
from .ui.ui_rf_power_panel import Ui_RFPowerPanel

logger = logging.getLogger(__name__)


class RFPowerPanel(Ui_RFPowerPanel, QtWidgets.QGroupBox):
    def __init__(self, controller: DeviceController,
                 parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.controller = controller

        self.setupUi(self)  # type: ignore

        self.controller.rf_power_changed.connect(self.rf_power_changed_cb)

        self.rf_power_changed_cb(
            controller, self.controller.get_rf_power_status())

        self.enableButton.clicked.connect(self.controller.enable_rf_power)
        self.disableButton.clicked.connect(self.controller.disable_rf_power)

    def add_ctrl_var_widget(self, widget: QtWidgets.QWidget) -> None:
        self.ctrlVarLayout.addWidget(widget)

    def clear_ctrl_var_widgets(self) -> None:
        while True:
            item = self.ctrlVarLayout.takeAt(0)
            if not item:
                break
            # NOTE: the items are deleted by the caller

    @QtCore.Slot(object, object)
    def rf_power_changed_cb(self, _controller: DeviceController,
                            status: RFPowerStatus) -> None:
        if status == RFPowerStatus.NOT_SUPPORTED:
            # NOTE: this state happens during device close
            self.enableButton.setEnabled(False)
            self.disableButton.setEnabled(False)
        elif status == RFPowerStatus.ENABLED:
            self.enableButton.setEnabled(False)
            self.disableButton.setEnabled(True)
        else:
            self.enableButton.setEnabled(True)
            self.disableButton.setEnabled(False)
