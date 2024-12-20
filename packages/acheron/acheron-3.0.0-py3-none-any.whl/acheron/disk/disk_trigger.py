from typing import Any, Optional

from pydantic import (BaseModel, Field, field_validator, model_validator,
                      ValidationInfo)

from ..calc_process.types import LimitType, Trigger


class DiskTrigger(BaseModel):
    serial: tuple[str, ...]
    id: str
    channel_id: int
    subchannel_index: int = 0
    limit_type: LimitType
    activate_limit: float  # specifies leading edge threshold
    deactivate_limit: Optional[float] = None
    hysteresis: Optional[float] = Field(ge=0.0, default=None, exclude=True,
                                        repr=False)

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
    def has_deactivate(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "deactivate_limit" in data and "hysteresis" in data:
                raise ValueError("deactivate_limit and hysteresis both set")
        return data

    @model_validator(mode='after')
    def convert_hysteresis(self):  # type: ignore
        if self.deactivate_limit is None:
            if self.hysteresis is None:
                raise ValueError("deactivate_limit or hysteresis missing")

            # get it from hysteresis
            if (self.limit_type == LimitType.MEAN_HIGH_LIMIT or
                    self.limit_type == LimitType.STD_HIGH_LIMIT):
                delta = -self.hysteresis
            elif (self.limit_type == LimitType.MEAN_LOW_LIMIT or
                    self.limit_type == LimitType.STD_LOW_LIMIT):
                delta = self.hysteresis
            else:
                raise ValueError("Unknown limit type for hysteresis")

            self.deactivate_limit = self.activate_limit + delta
            self.hysteresis = None
        else:
            if (self.limit_type == LimitType.MEAN_HIGH_LIMIT or
                    self.limit_type == LimitType.STD_HIGH_LIMIT):
                if self.deactivate_limit > self.activate_limit:
                    raise ValueError(
                        "deactivate_limit greater than activate_limit")
            elif (self.limit_type == LimitType.MEAN_LOW_LIMIT or
                    self.limit_type == LimitType.STD_LOW_LIMIT):
                if self.deactivate_limit < self.activate_limit:
                    raise ValueError(
                        "deactivate_limit less than activate_limit")
            else:
                # don't know, ignore and hope the user knows
                pass

        return self

    def convert(self) -> Trigger:
        values = self.model_dump()
        del values["serial"]
        return Trigger(**values)
