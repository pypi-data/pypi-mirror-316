from dataclasses import dataclass
import logging
import queue
import threading
from typing import Any

from hyperborea.event_database import log_event

from ..device_logging import DeviceLoggerAdapter
from ..core.preferences import Preferences

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Event:
    serial_number: str
    category: str
    description: str
    data: dict[str, Any]


class EventUploader:
    def __init__(self, preferences: Preferences):
        self.preferences = preferences

        self.event_queue: queue.Queue[Event] = queue.Queue()

        self.is_finished = threading.Event()
        self.upload_thread = threading.Thread(target=self._upload_loop)
        self.upload_thread.start()

    def stop(self) -> None:
        self.is_finished.set()

    def join(self) -> None:
        self.upload_thread.join()

    def firmware_updated(self, serial_number: str, success: bool,
                         event_data: dict[str, Any]) -> None:
        event_data['success'] = success

        if not success:
            description = "Firmware Update Failed"
        else:
            build_info = event_data.get('build_info')
            if build_info:
                description = f"Firmware Update with {build_info}"
            else:
                description = "Firmware Update"

        event = Event(
            serial_number=serial_number,
            category="Firmware Update",
            description=description,
            data=event_data)

        if self.preferences.event_upload_enabled:
            self.event_queue.put_nowait(event)

    def calibration_finished(self, serial_number: str,
                             event_data: dict[str, Any]) -> None:
        event = Event(
            serial_number=serial_number,
            category="Calibration",
            description="Calibration",
            data=event_data)

        if self.preferences.event_upload_enabled:
            self.event_queue.put_nowait(event)

    def _upload_event(self, event: Event) -> None:
        # do the upload
        try:
            log_event(event.serial_number, event.category, event.description,
                      **event.data)
        except Exception:
            device_logger = DeviceLoggerAdapter(logger, event.serial_number)
            device_logger.exception("Error uploading event")

    def _upload_loop(self) -> None:
        try:
            while not self.is_finished.is_set():
                try:
                    event = self.event_queue.get(True, 0.5)
                except queue.Empty:
                    continue

                self._upload_event(event)
        except Exception:
            logger.exception("Uncaught exception in event_upload_loop")
