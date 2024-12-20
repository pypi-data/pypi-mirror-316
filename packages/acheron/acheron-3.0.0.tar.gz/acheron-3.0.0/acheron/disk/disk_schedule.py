from datetime import datetime, timedelta
from functools import cache
import hashlib
import re
from typing import Any, Optional
from zoneinfo import ZoneInfo

from croniter import croniter
from pydantic import (AwareDatetime, BaseModel, field_validator,
                      model_validator, ValidationInfo)

from ..device_process.schedule import ScheduleItem


class DiskSchedule(BaseModel, frozen=True):
    serial: tuple[str, ...]

    remote_bootloader: bool = False

    trigger: Optional[str] = None

    needs_rf_power: bool = False

    active_streams: Optional[frozenset[int]] = None  # None means all available

    device_config: frozenset[tuple[str, Any]] = frozenset()

    start_time: Optional[AwareDatetime] = None
    stop_time: Optional[AwareDatetime] = None
    duration: Optional[timedelta] = None
    failure_delay: Optional[timedelta] = None

    cron_start: Optional[str] = None
    cron_timezone: Optional[str] = None

    @field_validator('serial', mode="before")
    @classmethod
    def ensure_list(cls, v: str, info: ValidationInfo) -> tuple[str, ...]:
        if isinstance(v, str):
            if len(v) > 0:
                return (v,)
            else:
                raise ValueError("Empty serial number string")
        else:
            if len(v) == 0:
                raise ValueError("Empty serial number")
            return v

    @model_validator(mode='before')
    @classmethod
    def _cron_exclusion(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data.get("cron_start", None) is not None:
                if data.get('start_time', None) is not None:
                    raise ValueError("cron_start set with start_time")
                if data.get('stop_time', None) is not None:
                    raise ValueError("cron_start set with stop_time")
                if data.get('duration', None) is None:
                    raise ValueError("cron_start set without duration")
        return data

    @model_validator(mode='before')
    @classmethod
    def _has_cron_timezone_with_start(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data.get("cron_timezone", None) is not None:
                if data.get("cron_start", None) is None:
                    raise ValueError("cron_timezone set without cron_start")
        return data

    @model_validator(mode='before')
    @classmethod
    def _has_failure_delay_with_start(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data.get("failure_delay", None) is not None:
                if (data.get("start_time", None) is None and
                        data.get("cron_start", None) is None):
                    raise ValueError(
                        "failure_delay set without start_time or cron_start")
        return data

    @field_validator('cron_timezone')
    @classmethod
    def _check_timezone(cls, v: Optional[str],
                        _info: ValidationInfo) -> Optional[str]:
        if v is None:
            return None
        else:
            # will raise an exception if wrong
            ZoneInfo(v)
            return v

    @field_validator('cron_start')
    @classmethod
    def _cron_valid(cls, v: str, _info: ValidationInfo) -> str:
        if isinstance(v, str):
            if not croniter.is_valid(v, hash_id=b"validate"):
                raise ValueError("Invalid cron string")
        return v

    def is_single_item(self) -> bool:
        return self.cron_start is None

    @cache
    def get_base_id(self) -> str:
        json_string = self.model_dump_json()
        hash_object = hashlib.sha256(json_string.encode())
        return "ds-" + hash_object.hexdigest()

    @staticmethod
    def _get_remote_sn(serial: tuple[str, ...]) -> Optional[int]:
        if len(serial) < 2:
            return None
        matches = re.findall(r'\d+', serial[-1])
        return int(matches[-1]) if matches else None

    def convert_single_item(self) -> ScheduleItem:
        values = self.model_dump()
        values['remote_sn'] = self._get_remote_sn(values["serial"])
        del values["serial"]
        del values["cron_start"]
        del values["cron_timezone"]

        failure_delay = values.pop("failure_delay", None)
        if failure_delay:
            values["failure_time"] = self.start_time + failure_delay

        return ScheduleItem(id=self.get_base_id(), output_config=True,
                            **values)

    def convert_cron(self, start_time: datetime) -> ScheduleItem:
        values = self.model_dump()
        values['remote_sn'] = self._get_remote_sn(values["serial"])
        del values["serial"]
        del values["cron_start"]
        del values["cron_timezone"]

        values['start_time'] = start_time

        failure_delay = values.pop("failure_delay", None)
        if failure_delay:
            values["failure_time"] = start_time + failure_delay

        id = self.get_base_id() + " " + start_time.isoformat()

        return ScheduleItem(id=id, output_config=True, **values)

    def get_base_serial(self) -> tuple[str, ...]:
        if len(self.serial) >= 2:
            return self.serial[:-1]
        else:
            return self.serial
