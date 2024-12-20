import logging
from typing import Optional, Union

from PySide6 import QtCore, QtWidgets

from ..device_process.stream_controller import (
    RFFixedTestParams, RFSweepTestParams)

from .ui.ui_rf_test_dialog import Ui_RFTestDialog

logger = logging.getLogger(__name__)


class RFTestDialog(Ui_RFTestDialog, QtWidgets.QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup()

    def extra_ui_setup(self) -> None:
        self.test_type_group = QtWidgets.QButtonGroup(self)
        self.test_type_group.addButton(self.fixedRadioButton)
        self.test_type_group.addButton(self.sweepRadioButton)

        self.test_mode_group = QtWidgets.QButtonGroup(self)
        self.test_mode_group.addButton(self.txCarrierRadioButton)
        self.test_mode_group.addButton(self.rxCarrierRadioButton)
        self.test_mode_group.addButton(self.txModulatedRadioButton)

        self.fixedChannel.editingFinished.connect(self.check_channels)
        self.startChannel.editingFinished.connect(self.check_channels)
        self.stopChannel.editingFinished.connect(self.check_channels)
        self.fixedChannel.valueChanged.connect(self.update_frequencies)
        self.startChannel.valueChanged.connect(self.update_frequencies)
        self.stopChannel.valueChanged.connect(self.update_frequencies)

        self.fixedRadioButton.setChecked(True)
        self.txCarrierRadioButton.setChecked(True)

    @QtCore.Slot()
    def check_channels(self) -> None:
        fixed_channel = self.fixedChannel.value()
        if fixed_channel % 2 != 0:
            fixed_channel -= 1
            self.fixedChannel.setValue(fixed_channel)
        start_channel = self.startChannel.value()
        if start_channel % 2 != 0:
            start_channel -= 1
            self.startChannel.setValue(start_channel)
        stop_channel = self.stopChannel.value()
        if stop_channel % 2 != 0:
            stop_channel -= 1
            self.stopChannel.setValue(stop_channel)

    @QtCore.Slot()
    def update_frequencies(self) -> None:
        fixed_channel = self.fixedChannel.value()
        self.centerFreq.setText("{} MHz".format(fixed_channel + 2400))
        start_channel = self.startChannel.value()
        self.startFreq.setText("{} MHz".format(start_channel + 2400))
        stop_channel = self.stopChannel.value()
        self.stopFreq.setText("{} MHz".format(stop_channel + 2400))

    def get_test_params(self) -> Union[RFFixedTestParams, RFSweepTestParams]:
        if self.txCarrierRadioButton.isChecked():
            mode = 0
        elif self.rxCarrierRadioButton.isChecked():
            mode = 1
        else:  # self.txModulatedRadioButton.isChecked()
            mode = 2

        if self.fixedRadioButton.isChecked():
            return RFFixedTestParams(
                channel=self.fixedChannel.value(),
                duration=self.fixedDuration.value(),
                mode=mode,
            )
        else:  # self.sweepRadioButton.isChecked()
            return RFSweepTestParams(
                start=self.startChannel.value(),
                stop=self.stopChannel.value(),
                hop_interval=self.hopInterval.value(),
                hop_count=self.hopCount.value(),
                mode=mode,
            )
