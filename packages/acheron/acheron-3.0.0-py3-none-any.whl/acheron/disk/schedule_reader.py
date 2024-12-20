from collections import deque
from datetime import datetime, timedelta, timezone
from functools import cache
import logging
import os
import threading
from zoneinfo import ZoneInfo

from PySide6 import QtCore

from croniter import croniter, CroniterBadDateError
from pydantic import TypeAdapter

from .disk_schedule import DiskSchedule
from .disk_trigger import DiskTrigger
from ..calc_process.types import Trigger
from ..core.device_controller import DeviceController
from ..core.dispatcher import Dispatcher
from ..device_process.schedule import ScheduleItem

logger = logging.getLogger(__name__)


SCHEDULE_READER_KEY = "schedule_reader"


GlobalSchedule = dict[tuple[str, ...], list[DiskSchedule]]


class ScheduleReader(QtCore.QObject):
    error = QtCore.Signal(str)
    warning = QtCore.Signal(str)

    _cron_schedule_updated = QtCore.Signal()

    def __init__(self, basedir: str, dispatcher: Dispatcher):
        super().__init__()

        self.dispatcher = dispatcher
        self.basedir = basedir

        self.trigger_filename = os.path.join(self.basedir, "triggers.json")
        self.schedule_filename = os.path.join(
            self.basedir, "schedule_items.json")
        self.timedelta = timedelta(seconds=120)

        self.lock = threading.Lock()
        self.controllers: dict[tuple[str, ...], DeviceController] = {}
        self.cron_schedule: GlobalSchedule = {}
        self.last_cron_stop: datetime = datetime.now(timezone.utc)
        self.finished = threading.Event()
        self.cron_deque: deque[tuple[tuple[str, ...],
                                     list[ScheduleItem]]] = deque()

        self.cron_thread = threading.Thread(target=self._cron_thread_run)
        self.cron_thread.start()

        self._cron_schedule_updated.connect(self._cron_schedule_updated_cb)

    def start(self) -> None:
        self._read_all()

    def stop(self) -> None:
        self.finished.set()
        self.cron_thread.join()

    def reload(self) -> None:
        self._read_all()

    @staticmethod
    def _read_triggers(trigger_filename: str) -> \
            tuple[dict[tuple[str, ...], set[Trigger]], set[str]]:
        try:
            with open(trigger_filename, "rt") as f:
                contents = f.read()
        except FileNotFoundError:
            return ({}, set())

        ta = TypeAdapter(list[DiskTrigger])
        triggers = ta.validate_json(contents)

        trigger_dict: dict[tuple[str, ...], set[Trigger]] = {}
        trigger_names: set[str] = set()
        for t in triggers:
            trigger_names.add(t.id)
            trigger_set = trigger_dict.get(t.serial)
            if not trigger_set:
                trigger_set = set((t.convert(),))
                trigger_dict[t.serial] = trigger_set
            else:
                trigger_set.add(t.convert())

        return trigger_dict, trigger_names

    @staticmethod
    def _read_schedule_items(schedule_filename: str) -> tuple[
            GlobalSchedule, GlobalSchedule, set[tuple[str, ...]]]:
        try:
            with open(schedule_filename, "rt") as f:
                contents = f.read()
        except FileNotFoundError:
            return {}, {}, set()

        ta = TypeAdapter(list[DiskSchedule])
        schedule_items = ta.validate_json(contents)

        now = datetime.now(timezone.utc)

        single_schedule: GlobalSchedule = {}
        cron_schedule: GlobalSchedule = {}
        all_serials: set[tuple[str, ...]] = set()
        for schedule_item in schedule_items:
            if schedule_item.start_time and now > schedule_item.start_time:
                # too old
                continue

            all_serials.add(schedule_item.serial)
            serial = schedule_item.get_base_serial()  # doesn't include WM
            if schedule_item.is_single_item():
                schedule_list = single_schedule.setdefault(serial, [])
            else:
                schedule_list = cron_schedule.setdefault(serial, [])
            schedule_list.append(schedule_item)

        return single_schedule, cron_schedule, all_serials

    @staticmethod
    def _check_missing_triggers(schedule_items: GlobalSchedule,
                                trigger_names: set[str]) -> None:
        for schedule_list in schedule_items.values():
            for schedule_item in schedule_list:
                if schedule_item.trigger:
                    if schedule_item.trigger not in trigger_names:
                        logger.warning("Unknown trigger name %s",
                                       schedule_item.trigger)

    def _read_all(self) -> None:
        try:
            triggers, trigger_names = self._read_triggers(
                self.trigger_filename)
        except Exception:
            message = "Could not parse triggers"
            logger.exception(message)
            self.error.emit(message)
            return

        try:
            single_schedule, cron_schedule, schedule_serials = \
                self._read_schedule_items(self.schedule_filename)
        except Exception:
            message = "Could not parse schedule items"
            logger.exception(message)
            self.error.emit(message)
            return

        self._check_missing_triggers(single_schedule, trigger_names)
        self._check_missing_triggers(cron_schedule, trigger_names)

        with self.lock:
            serials = set(triggers) | schedule_serials
            old_serials = set(self.controllers)

            unused_serials = old_serials.difference(serials)
            new_serials = serials.difference(old_serials)

            for serial in unused_serials:
                controller = self.controllers.pop(serial)
                controller.register_triggers(SCHEDULE_READER_KEY, set())
                controller.schedule.clear_partition(SCHEDULE_READER_KEY)
                controller.release_party(SCHEDULE_READER_KEY)

            for serial in new_serials:
                controller = self.dispatcher.get_controller(
                    serial, SCHEDULE_READER_KEY)
                self.controllers[serial] = controller

            for serial in serials:
                controller = self.controllers[serial]
                device_triggers = triggers.get(serial)
                if device_triggers is None:
                    device_triggers = set()
                controller.register_triggers(
                    SCHEDULE_READER_KEY, device_triggers)

                single_list = single_schedule.get(serial)
                if single_list:
                    controller.schedule.set_partition_items(
                        SCHEDULE_READER_KEY,
                        (i.convert_single_item() for i in single_list))
                else:
                    controller.schedule.clear_partition(SCHEDULE_READER_KEY)

            self.cron_schedule = cron_schedule
            self.cron_deque.clear()  # in case any were created before locking
            start = datetime.now(timezone.utc)
            stop = start + self.timedelta
            self.last_cron_stop = stop
            self._single_pass(start, stop)
            updated = bool(self.cron_deque)

        if updated:
            self._cron_schedule_updated.emit()

    @staticmethod
    def _croniter_range(start: datetime, stop: datetime, expr_format: str,
                        hash_id: bytes) -> list[datetime]:
        """Slimmed down version of croniter_range() that supports hash_id, and
        is inclusive with stop end"""
        ic = croniter(expr_format, start, ret_type=datetime,
                      max_years_between_matches=1, hash_id=hash_id)
        values: list[datetime] = []
        try:
            dt = ic.get_next()
            while dt <= stop:
                values.append(dt)
                dt = ic.get_next()
        except CroniterBadDateError:
            pass

        return values

    @staticmethod
    @cache
    def _get_tz(timezone_name: str) -> ZoneInfo:
        return ZoneInfo(timezone_name)

    def _single_pass(self, start: datetime, stop: datetime) -> None:  # locked
        for serial_number, schedule_list in self.cron_schedule.items():
            for schedule_item in schedule_list:
                base_id = schedule_item.get_base_id()
                hash_id = base_id.encode("utf-8")
                expr_format: str = schedule_item.cron_start  # type: ignore
                if schedule_item.cron_timezone:
                    tz = self._get_tz(schedule_item.cron_timezone)
                    datetimes = self._croniter_range(
                        start.astimezone(tz), stop.astimezone(tz),
                        expr_format, hash_id)
                else:
                    datetimes = self._croniter_range(
                        start, stop, expr_format, hash_id)

                new_items = [schedule_item.convert_cron(d) for d in datetimes]
                if new_items:
                    self.cron_deque.append((serial_number, new_items))

    def _cron_thread_run(self) -> None:
        while not self.finished.wait(timeout=60):
            with self.lock:
                start = self.last_cron_stop
                stop = datetime.now(timezone.utc) + self.timedelta
                self.last_cron_stop = stop
                self._single_pass(start, stop)

                updated = bool(self.cron_deque)

            if updated:
                self._cron_schedule_updated.emit()

    @QtCore.Slot()
    def _cron_schedule_updated_cb(self) -> None:
        with self.lock:
            while self.cron_deque:
                serial_number, schedule_list = self.cron_deque.popleft()
                controller = self.controllers[serial_number]
                for schedule_item in schedule_list:
                    controller.schedule.add_item(
                        SCHEDULE_READER_KEY, schedule_item)
