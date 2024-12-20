from dataclasses import dataclass
import enum
from typing import Any

from asphodel import AsphodelChannelInfo, StreamRateInfo


@dataclass()
class ChannelInformation:
    name: str
    channel_id: int
    stream_id: int
    channel: AsphodelChannelInfo
    subchannel_names: list[str]
    rate_info: StreamRateInfo
    samples: int
    rate: float
    downsample_factor: int
    mean_len: int
    plot_len: int
    fft_shortened: bool
    fft_sample_len: int
    fft_freq_axis: Any
    fft_size: int


@enum.unique
class CalcData(enum.Enum):
    PROCESSING_START = enum.auto()
    PROCESSING_STOP = enum.auto()
    CHANNEL_UPDATE = enum.auto()
    PLOT_UPDATE = enum.auto()
    FFT_UPDATE = enum.auto()
    LOST_PACKET_UPDATE = enum.auto()
    UNKNOWN_ID = enum.auto()
    ACTIVE_TRIGGERS_CHANGED = enum.auto()


@enum.unique
class CalcControl(enum.Enum):
    STOP = enum.auto()  # stop packet processing, but still pull from the pipe
    CLOSE = enum.auto()
    SET_SHOWN = enum.auto()
    PLOT_CHANGE = enum.auto()
    RESET_LOST_PACKETS = enum.auto()
    CHANGE_SETTINGS = enum.auto()
    CHANGE_TRIGGERS = enum.auto()
    SET_CONNECTIVITY_PIPE = enum.auto()


@dataclass()
class CalcSettings:
    channel_interval: float
    plot_interval: float
    fft_interval: float
    downsample: bool


@enum.unique
class LimitType(enum.Enum):
    MEAN_HIGH_LIMIT = 'mean high'
    MEAN_LOW_LIMIT = 'mean low'
    STD_HIGH_LIMIT = 'std high'
    STD_LOW_LIMIT = 'std low'


@dataclass(eq=True, frozen=True)
class Trigger:
    id: str
    channel_id: int
    subchannel_index: int
    limit_type: LimitType

    # NOTE: for MEAN_HIGH_LIMIT or STD_HIGH_LIMIT you'd want activate_limit
    # to be greater than or equal to deactivate_limit. For MEAN_LOW_LIMIT or
    # STD_LOW_LIMIT, you'd want activate_limit to be less than or equal to
    # deactivate_limit.

    activate_limit: float  # specifies leading edge threshold
    deactivate_limit: float  # specifies trailing edge threshold
