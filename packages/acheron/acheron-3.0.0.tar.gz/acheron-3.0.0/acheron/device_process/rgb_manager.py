from typing import Callable, Optional

import asphodel
from asphodel.device_info import DeviceInfo


RGBCallback = Callable[[int, tuple[int, int, int]], None]


class RGBManager:
    def __init__(self, device: asphodel.AsphodelNativeDevice, auto_rgb: bool,
                 callback: RGBCallback):
        self.device = device
        self.auto_rgb = auto_rgb
        self.callback = callback

        self.device_info: Optional[DeviceInfo] = None

    def set_auto_rgb_locked(self, auto_rgb: bool) -> None:
        self.auto_rgb = auto_rgb

    def set_rgb_locked(self, index: int, values: tuple[int, int, int],
                       instant: bool = False) -> None:
        if self.device_info:
            if len(self.device_info.rgb_settings) > index:
                if self.device_info.rgb_settings[index] != values:
                    self.device_info.rgb_settings[index] = values
                    self.device.set_rgb_values(index, values, instant=instant)
                    self.callback(index, values)

    def connected_locked(self, device_info: DeviceInfo) -> None:
        self.device_info = device_info
        if self.auto_rgb:
            if device_info.supports_radio:
                self.set_rgb_locked(0, (0, 255, 255))  # cyan
            else:
                self.set_rgb_locked(0, (0, 0, 255))  # blue

    def streaming_locked(self) -> None:
        if self.auto_rgb and self.device_info:
            if self.device_info.supports_radio:
                pass  # don't change the RGB state for only local streaming
            else:
                self.set_rgb_locked(0, (0, 255, 0))  # green

    def disconnected_locked(self) -> None:
        if self.auto_rgb:
            self.set_rgb_locked(0, (255, 0, 0), instant=True)  # red
        self.device_info = None

    def remote_connected_locked(self) -> None:
        if self.auto_rgb:
            self.set_rgb_locked(0, (0, 255, 0))  # green

    def remote_disconnected_locked(self) -> None:
        if self.auto_rgb:
            self.set_rgb_locked(0, (0, 255, 255))  # cyan
