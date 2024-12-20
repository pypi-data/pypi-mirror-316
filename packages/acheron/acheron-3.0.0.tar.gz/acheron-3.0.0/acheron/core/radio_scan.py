from __future__ import annotations
import logging
from typing import Iterable, Optional, TYPE_CHECKING

from PySide6 import QtCore

from asphodel.device_info import ActiveScanInfo

from .preferences import Preferences
from ..device_process.stream_controller import ScanResult

if TYPE_CHECKING:
    from .device_controller import DeviceController

logger = logging.getLogger(__name__)


class ActiveScanDatabase(QtCore.QObject):
    cleared = QtCore.Signal()
    active_scan_ready = QtCore.Signal(int, object)  # remote, active_scan
    remote_connecting = QtCore.Signal(int, object)  # remote, controller/none

    def __init__(self, preferences: Preferences) -> None:
        super().__init__()

        self.preferences = preferences

        self.active_scan_desired = self.preferences.background_active_scan

        self.controller_remotes: dict[DeviceController, int] = {}
        self.active_scan_ongoing: dict[DeviceController, int] = {}

        self.active_scans: dict[int, ActiveScanInfo] = {}

    @QtCore.Slot(object)
    def controller_disconnected(self, controller: DeviceController) -> None:
        try:
            remote = self.controller_remotes.pop(controller)
            self.remote_connecting.emit(remote, None)
        except KeyError:
            pass

        try:
            del self.active_scan_ongoing[controller]
        except KeyError:
            pass

    @QtCore.Slot(object, int, bool)
    def controller_remote_connecting(self, controller: DeviceController,
                                     remote: int, _bootloader: bool) -> None:

        self.controller_remotes[controller] = remote
        self.remote_connecting.emit(remote, controller)

    @QtCore.Slot(object, object)
    def controller_scans(self, controller: DeviceController,
                         scans: Iterable[ScanResult]) -> None:
        try:
            # a set of scans means this controller isn't connected to a remote
            remote = self.controller_remotes.pop(controller)
            self.remote_connecting.emit(remote, None)
        except KeyError:
            pass

        if controller in self.active_scan_ongoing:
            # this controller was already sent an active scan requset
            return

        ongoing_scan_serials = set(self.active_scan_ongoing.values())

        for scan in scans:
            if scan.serial_number in self.active_scans:
                # already have it
                continue

            if scan.serial_number in ongoing_scan_serials:
                # someone is already scanning it
                continue

            if scan.bootloader:
                # don't active scan bootloaders as it causes issues
                continue

            if scan.board_info and not self.active_scan_desired:
                # don't need to do any background active scan
                continue

            self.active_scan_ongoing[controller] = scan.serial_number
            controller.start_active_scan(scan.serial_number, scan.bootloader)
            break

    @QtCore.Slot(object, int, object)
    def active_scan_finished(self, controller: DeviceController, remote: int,
                             active_scan: Optional[ActiveScanInfo]) -> None:
        try:
            del self.active_scan_ongoing[controller]
        except KeyError:
            pass

        if active_scan:
            self.active_scans[remote] = active_scan

            self.active_scan_ready.emit(remote, active_scan)

    def clear_database(self) -> None:
        self.active_scans.clear()
        self.cleared.emit()

    def get_remote_controller(self, remote: int) -> Optional[DeviceController]:
        for controller, r in self.controller_remotes.items():
            if r == remote:
                return controller

        return None

    def get_active_scan(self, remote: int) -> Optional[ActiveScanInfo]:
        return self.active_scans.get(remote)

    def detail_scan_opened(self) -> None:
        self.active_scan_desired = True

    def detail_scan_closed(self) -> None:
        self.active_scan_desired = self.preferences.background_active_scan
