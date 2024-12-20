import bisect
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
import logging
import threading
from typing import Any, Iterable, Literal, Optional, Union

import asphodel.device_config
from asphodel.device_info import DeviceInfo

logger = logging.getLogger(__name__)

min_dt = datetime.min.replace(tzinfo=timezone.utc)


@dataclass(frozen=True)
class OutputConfig:
    compression_level: int
    base_name: Optional[str]  # None means use the device's display name
    base_directory: str  # typically "Acheron Data"
    device_directory: Union[str, bool]  # False: no dir, True: display name
    date_dir_structure: bool  # use intermediate date directories
    datetime_filename: bool  # prefix filename with datetime
    roll_over_interval: Optional[timedelta]
    upload_marker: bool


@dataclass(eq=True, frozen=True)
class ScheduleItem:
    id: str
    remote_sn: Optional[int] = None
    remote_bootloader: bool = False

    trigger: Optional[str] = None

    needs_rf_power: bool = False

    active_streams: Optional[frozenset[int]] = frozenset()  # None means all

    # can't be a dict for mutability reasons, so use a frozenset of tuples
    device_config: frozenset[tuple[str, Any]] = frozenset()

    # These set when things happen. NOTE: some combinations don't make sense.
    #
    # For a "normal" timed collection, you'd set a collection_time, a
    # start_time a bit before the collection time, and a duration. The
    # stop_time would be None or the drop dead time. The failure_time would be
    # set some appropriate time into the future. For example an hour later.
    #
    # start_time -> The time to connect to device. None means -infinity (i.e.
    #               start right now).
    # collection_time -> The time to start writing packets to the file. None
    #                    means as soon as the connection is established.
    # _collection_time_internal -> The time where first packet went into the
    #                              file. Can't be None.
    # stop_time -> The time to stop writing packets to the file. None means
    #              +infinity (i.e. never).
    # duration -> Used to calculate _stop_time_target. None means +infinity.
    # failure_time -> Time used to remove this item from the schedule with an
    #                 error. None means +infinity.
    # _stop_time_target -> Minimum of [(_collection_time_internal+duration),
    #                      stop_time, failure_time]. This is used to check the
    #                      last packet in the file. If it's None, then
    #                      duration, stop_time and failure_time must all be
    #                      None, and this item will never be removed from the
    #                      schedule.
    start_time: Optional[datetime] = None
    collection_time: Optional[datetime] = None
    stop_time: Optional[datetime] = None
    duration: Optional[timedelta] = None
    failure_time: Optional[datetime] = None

    # how the files get written, (None means no archiving, True means default)
    output_config: Union[OutputConfig, None, Literal[True]] = None

    def configure_nvm(self, device_info: DeviceInfo, nvm: bytes) -> bytes:
        return asphodel.device_config.configure_nvm(
            self.device_config, device_info, nvm)

    def nvm_valid(self, device_info: DeviceInfo, nvm: bytes) -> bool:
        new_nvm = self.configure_nvm(device_info, nvm)
        return new_nvm == nvm

    def priority_key(self) -> tuple:
        # sort by end time, sooner ones earlier, and None last
        # sort within those by duration, shorter earlier, and None last
        return (
            self.stop_time is None,
            self.stop_time,
            self.duration is None,
            self.duration,
            float('inf') if self.remote_sn is None else self.remote_sn,
        )

    def sort_key(self) -> tuple:
        return (
            min_dt if self.start_time is None else self.start_time,
            float('inf') if self.remote_sn is None else self.remote_sn,
        )

    def __lt__(self, other: "ScheduleItem") -> bool:
        return self.sort_key() < other.sort_key()

    def __le__(self, other: "ScheduleItem") -> bool:
        return self.sort_key() <= other.sort_key()

    def __gt__(self, other: "ScheduleItem") -> bool:
        return self.sort_key() > other.sort_key()

    def __ge__(self, other: "ScheduleItem") -> bool:
        return self.sort_key() >= other.sort_key()


def get_compatible_set(items: Iterable[ScheduleItem], device_info: DeviceInfo,
                       nvm: bytes) -> tuple[set[ScheduleItem], bytes,
                                            Optional[tuple[int, bool]]]:
    # sort by end time, sooner ones earlier, and None last
    items = sorted(items, key=ScheduleItem.priority_key)

    best_nvm = nvm
    current_items: set[ScheduleItem] = set()
    remote = None

    for item in items:
        if item.remote_sn is not None:
            if remote is None:
                remote = (item.remote_sn, item.remote_bootloader)
            continue

        new_nvm = item.configure_nvm(device_info, best_nvm)

        # quick cheat, if nvm hasn't changed there's no need to recheck
        if new_nvm == best_nvm:
            current_items.add(item)
            continue

        # check that every current item is happy with the new nvm
        valid = True
        for current_item in current_items:
            if not current_item.nvm_valid(device_info, new_nvm):
                valid = False
                break

        if valid:
            current_items.add(item)
            best_nvm = new_nvm

    return current_items, best_nvm, remote


class Schedule:
    def __init__(self, schedule_items: Iterable[ScheduleItem],
                 active_triggers: frozenset[str]):
        self.active_triggers = active_triggers

        self.lock = threading.Lock()

        # this is kept sorted
        self.schedule_items = sorted(schedule_items)

    def __len__(self) -> int:
        with self.lock:
            return len(self.schedule_items)

    def remote_len(self, remote: int) -> int:
        total = 0
        with self.lock:
            for schedule_item in self.schedule_items:
                if schedule_item.remote_sn == remote:
                    total += 1
        return total

    def _delete_item_id(self, item_id: str) -> None:  # call with lock
        for i, check_item in enumerate(self.schedule_items):
            if check_item.id == item_id:
                del self.schedule_items[i]
                return
        # don't raise any error when the item is missing

    def delete_item_id(self, item_id: str) -> None:
        with self.lock:
            self._delete_item_id(item_id)

    def _update_item(self, item: ScheduleItem) -> None:  # call with lock
        # delete old one, if present
        self._delete_item_id(item.id)

        # add it
        bisect.insort(self.schedule_items, item)

    def update_item(self, item: ScheduleItem) -> None:
        with self.lock:
            self._update_item(item)

    def update_items(self, schedule_items: Iterable[ScheduleItem]) -> None:
        with self.lock:
            # add in all the new ones
            for item in schedule_items:
                bisect.insort(self.schedule_items, item)

    def get_ready_items(self, remote: Optional[int] = None) -> tuple[
            set[ScheduleItem], Optional[float]]:
        with self.lock:
            ready: set[ScheduleItem] = set()
            now = None  # will be created only if needed

            for item in self.schedule_items:
                if remote is not None and item.remote_sn != remote:
                    continue

                if item.trigger and item.trigger not in self.active_triggers:
                    continue

                start_time = item.start_time
                if start_time is not None:
                    if now is None:
                        now = datetime.now(timezone.utc)
                    if now < start_time:
                        # list is sorted, everything left is too late
                        next_change = (start_time - now).total_seconds()
                        return (ready, next_change)
                ready.add(item)
            return (ready, None)

    def set_active_triggers(self, active_triggers: frozenset[str]) -> None:
        with self.lock:
            self.active_triggers = active_triggers

    def get_expired_items(self) -> set[ScheduleItem]:
        expired: set[ScheduleItem] = set()
        with self.lock:
            now = datetime.now(timezone.utc)
            stop_time = now - timedelta(seconds=10)
            for item in self.schedule_items:
                if item.failure_time and item.failure_time < now:
                    expired.add(item)
                elif item.stop_time and item.stop_time < stop_time:
                    expired.add(item)
        return expired


class RemoteSchedule:
    def __init__(self, schedule: Schedule, remote_sn: int,
                 remote_bootloader: bool,
                 schedule_items: Iterable[ScheduleItem]):
        self.schedule = schedule
        self.remote_sn = remote_sn
        self.remote_bootloader = remote_bootloader
        new_items = [self._convert_item_to_remote(i) for i in schedule_items]
        self.schedule.update_items(new_items)

    def __len__(self) -> int:
        return self.schedule.remote_len(self.remote_sn)

    def delete_item_id(self, item_id: str) -> None:
        self.schedule.delete_item_id(item_id)

    def _convert_item_to_remote(self, item: ScheduleItem) -> ScheduleItem:
        return replace(item, remote_sn=self.remote_sn,
                       remote_bootloader=self.remote_bootloader)

    def _convert_item_from_remote(self, item: ScheduleItem) -> ScheduleItem:
        return replace(item, remote_sn=None)

    def update_item(self, item: ScheduleItem) -> None:
        self.schedule.update_item(self._convert_item_to_remote(item))

    def get_ready_items(self) -> tuple[set[ScheduleItem], Optional[float]]:
        ready, next_change = self.schedule.get_ready_items(
            remote=self.remote_sn)
        return (set(self._convert_item_from_remote(i) for i in ready),
                next_change)

    def set_active_triggers(self, active_triggers: frozenset[str]) -> None:
        # do nothing here, let the main schedule keep track
        pass

    def get_expired_items(self) -> set[ScheduleItem]:
        # do nothing here, let the main schedule keep track
        return set()
