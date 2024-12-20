import datetime
import logging
from typing import Iterable, Optional

from PySide6 import QtCore

from ..device_process.schedule import ScheduleItem

logger = logging.getLogger(__name__)


class DeviceSchedule(QtCore.QObject):
    finished_item = QtCore.Signal(str, bool)  # id, success

    updated_item = QtCore.Signal(object)  # ScheduleItem
    deleted_items = QtCore.Signal(object)  # set[str]

    def __init__(self, parent_schedule: Optional["DeviceSchedule"]):
        super().__init__()

        self.parent_schedule = parent_schedule

        self.schedule_items: dict[str, dict[str, ScheduleItem]] = {}
        self.schedule_count: int = 0

    def get_items(self) -> set[ScheduleItem]:
        all_values: dict[str, ScheduleItem] = {}
        for schedule_dict in self.schedule_items.values():
            all_values.update(schedule_dict)
        return set(all_values.values())

    def _clear_schedule_id(self, id: str) -> None:
        for schedule_dict in self.schedule_items.values():
            try:
                del schedule_dict[id]
            except KeyError:
                pass

    def add_item(self, partition: str, schedule_item: ScheduleItem) -> None:
        schedule_items = self.schedule_items.setdefault(partition, {})
        schedule_items[schedule_item.id] = schedule_item

        self.updated_item.emit(schedule_item)

    def set_partition_items(self, partition: str,
                            schedule_items: Iterable[ScheduleItem]) -> None:
        try:
            old_schedule_items = self.schedule_items.pop(partition)
        except KeyError:
            # no problem
            old_schedule_items = {}

        new_schedule_items = {i.id: i for i in schedule_items}
        self.schedule_items[partition] = new_schedule_items

        ids_to_delete = set(old_schedule_items).difference(
            new_schedule_items)
        if ids_to_delete:
            self.deleted_items.emit(ids_to_delete)

        for schedule_item in new_schedule_items.values():
            old_schedule_item = old_schedule_items.get(schedule_item.id)
            if not old_schedule_item or old_schedule_item != schedule_item:
                self.updated_item.emit(schedule_item)

    def clear_partition(self, *partitions: str) -> None:
        ids: set[str] = set()
        for partition in partitions:
            try:
                old_schedule_items = self.schedule_items.pop(partition)
            except KeyError:
                # no problem
                continue

            for schedule_item in old_schedule_items.values():
                ids.add(schedule_item.id)

        if ids:
            self.deleted_items.emit(ids)

    def mark_finished(self, schedule_id: str, success: bool) -> None:
        self._clear_schedule_id(schedule_id)
        if self.parent_schedule is not None:
            self.parent_schedule._clear_schedule_id(schedule_id)

        self.finished_item.emit(schedule_id, success)

    def clear_expired_items(self) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        stop_time = now - datetime.timedelta(seconds=10)
        all_expried: set[str] = set()

        for schedule_dict in self.schedule_items.values():
            expired: set[str] = set()
            for schedule_id, item in schedule_dict.items():
                if item.failure_time and item.failure_time < now:
                    expired.add(schedule_id)
                elif item.stop_time and item.stop_time < stop_time:
                    expired.add(schedule_id)
            for schedule_id in expired:
                schedule_dict.pop(schedule_id)
                self.finished_item.emit(schedule_id, False)
            all_expried.update(expired)

        if all_expried:
            self.deleted_items.emit(all_expried)


class MainSchedule(QtCore.QObject):
    def __init__(self) -> None:
        super().__init__()

        self.schedules: dict[tuple[str, ...], DeviceSchedule] = {}
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timer_cb)
        self.timer.start(1000)  # 1 second intervals

    def get_schedule(self, serial_numbers: tuple[str, ...]) -> DeviceSchedule:
        try:
            return self.schedules[serial_numbers]
        except KeyError:
            # didn't find it
            pass

        if len(serial_numbers) == 0:
            raise ValueError("No serial numbers provided")
        elif len(serial_numbers) == 1:
            device_schedule = DeviceSchedule(None)
        elif len(serial_numbers) == 2:
            parent = self.get_schedule(serial_numbers[:-1])
            device_schedule = DeviceSchedule(parent)
        else:
            raise ValueError("Too many serial numbers provided")

        self.schedules[serial_numbers] = device_schedule
        return device_schedule

    @QtCore.Slot()
    def timer_cb(self) -> None:
        for device_schedule in self.schedules.values():
            device_schedule.clear_expired_items()
