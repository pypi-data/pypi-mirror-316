import datetime
import functools
import logging
import os
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

import asphodel
from asphodel import AsphodelStreamInfo, AsphodelChannelInfo, SupplyInfo

from asphodel.device_info import DeviceInfo

from ..device_logging import DeviceLoggerAdapter
from ..core.device_controller import DeviceController
from ..core.preferences import Preferences
from ..device_process.hardware_test_funcs import (
    accel_test, bridge_test, supply_test)
from ..device_process.stream_controller import HardwareTestFunction

from .ui.ui_hardware_tests import Ui_HardwareTestDialog

logger = logging.getLogger(__name__)


TestInstance = tuple[HardwareTestFunction, str]


class HardwareTestDialog(Ui_HardwareTestDialog, QtWidgets.QDialog):
    def __init__(self, device_info: DeviceInfo, controller: DeviceController,
                 preferences: Preferences, logger: DeviceLoggerAdapter,
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.device_info = device_info
        self.controller = controller
        self.preferences = preferences
        self.logger = logger

        self.tests: list[TestInstance]
        self.create_test_list()

        self.results: dict[str, bool] = {}

        self.setupUi(self)  # type: ignore

        self.test_log = ""
        self.testOutput.setPlainText(self.test_log)

        self.rerunButton = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Reset)
        self.rerunButton.setText(self.tr("Rerun Tests"))
        self.rerunButton.clicked.connect(self.start_tests)

        self.testOutput.setFont(QtGui.QFontDatabase.systemFont(
            QtGui.QFontDatabase.SystemFont.FixedFont))

    def _create_supply_test(self, supply_id: int, name: str,
                            info: SupplyInfo) -> TestInstance:
        func = functools.partial(
            supply_test, supply_id=supply_id, name=name, info=info)

        return (func, f"supply_{supply_id}")

    def _create_accel_test(
            self, stream_id: int, stream: AsphodelStreamInfo, channel_id: int,
            channel: AsphodelChannelInfo) -> TestInstance:
        func = functools.partial(
            accel_test, stream_id=stream_id, stream=stream,
            channel_id=channel_id, channel=channel)

        return (func, f"accel_{stream_id}_{channel_id}")

    def _create_bridge_test(
            self, stream_id: int, stream: AsphodelStreamInfo, channel_id: int,
            channel: AsphodelChannelInfo) -> TestInstance:
        func = functools.partial(
            bridge_test, stream_id=stream_id, stream=stream,
            channel_id=channel_id, channel=channel)

        return (func, f"bridge_{stream_id}_{channel_id}")

    def create_test_list(self) -> None:
        self.tests = []

        for i, (name, supply_info) in enumerate(self.device_info.supplies):
            self.tests.append(self._create_supply_test(i, name, supply_info))

        for stream_id, stream in enumerate(self.device_info.streams):
            channel_indexes = stream.channel_index_list[0:stream.channel_count]
            for channel_id in channel_indexes:
                if channel_id < len(self.device_info.channels):
                    channel = self.device_info.channels[channel_id]
                    ch_type = channel.channel_type
                    if (ch_type == asphodel.CHANNEL_TYPE_SLOW_ACCEL or
                            ch_type == asphodel.CHANNEL_TYPE_PACKED_ACCEL or
                            ch_type == asphodel.CHANNEL_TYPE_LINEAR_ACCEL):
                        self.tests.append(self._create_accel_test(
                            stream_id, stream, channel_id, channel))
                    elif (ch_type == asphodel.CHANNEL_TYPE_SLOW_STRAIN or
                            ch_type == asphodel.CHANNEL_TYPE_FAST_STRAIN or
                            ch_type == asphodel.CHANNEL_TYPE_COMPOSITE_STRAIN):
                        self.tests.append(self._create_bridge_test(
                            stream_id, stream, channel_id, channel))

    @QtCore.Slot()
    def start_tests(self) -> None:
        self.rerunButton.setEnabled(False)
        self.results = {}
        self.controller.run_hardware_tests(self.tests, self)

        # use ISO 8601 representation
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
        dt_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        start_message = f"*** Start of tests {dt_str} ***\n\n"
        self.test_log = start_message
        self.testOutput.setPlainText(self.test_log)

    def hardware_test_function_finished(self, test_id: str,
                                        data: tuple[bool, str]) -> None:
        success, message = data

        self.results[test_id] = success

        self.test_log += message + "\n"
        self.testOutput.setPlainText(self.test_log)

    def hardware_test_run_finished(self) -> None:
        self.rerunButton.setEnabled(True)

        if len(self.results) != len(self.tests):
            self.test_log += "\nMissing test results!\n"

        failures = sum(1 for x in self.results.values() if x is False)

        plural = "failures" if failures != 1 else "failure"
        self.test_log += f"\n{failures} {plural}\n\n"

        # use ISO 8601 representation
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
        dt_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        end_message = f"*** End of tests {dt_str} ***\n"
        self.test_log += end_message
        self.testOutput.setPlainText(self.test_log)

        self.save_test_log()

    def save_test_log(self) -> None:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
        dt_str = dt.strftime("%Y%m%dT%H%MZ_")
        directory = os.path.join(self.preferences.base_dir, "Hardware Tests")
        base_name = os.path.join(directory,
                                 dt_str + self.controller.serial_number)

        # create a unique filename, accounting for existing files
        filename = base_name + ".txt"
        index = 1
        while os.path.exists(filename):
            filename = base_name + "(" + str(index) + ").txt"
            index += 1

        self.logger.info("Test log saved: %s", filename)

        with open(filename, "wt") as f:
            f.write(self.test_log)
