import math
import struct

import asphodel
from ..device_logging import DeviceLoggerAdapter


def get_channel_setting_values(
        settings_len: int, cal: asphodel.ChannelCalibration,
        unit_type: int, scale: float,
        offset: float) -> tuple[dict[int, int], dict[int, float]]:
    unit_settings = {cal.base_setting_index: unit_type}
    float_settings = {cal.base_setting_index + 1: scale,
                      cal.base_setting_index + 2: offset}

    if math.isfinite(cal.minimum):
        minimum = cal.minimum * scale + offset
        float_settings[cal.base_setting_index + 3] = minimum

    if math.isfinite(cal.maximum):
        maximum = cal.maximum * scale + offset
        float_settings[cal.base_setting_index + 4] = maximum

    if cal.resolution_setting_index < settings_len:
        float_settings[cal.resolution_setting_index] = scale

    return unit_settings, float_settings


def update_nvm(nvm: bytes, settings: list[asphodel.AsphodelSettingInfo],
               unit_settings: dict[int, int], float_settings: dict[int, float],
               logger: DeviceLoggerAdapter) -> bytearray:
    nvm = bytearray(nvm)

    for setting_index, value in unit_settings.items():
        setting = settings[setting_index]
        if setting.setting_type != asphodel.SETTING_TYPE_UNIT_TYPE:
            msg = "Setting {} is not a unit type".format(setting_index)
            logger.error(msg)
        s = setting.u.byte_setting
        byte_offset = s.nvm_word * 4 + s.nvm_word_byte
        struct.pack_into(">B", nvm, byte_offset, value)

    for setting_index, f in float_settings.items():
        setting = settings[setting_index]
        if setting.setting_type == asphodel.SETTING_TYPE_INT32_SCALED:
            s_scaled = setting.u.int32_scaled_setting
            unscaled_i = int(round((f - s_scaled.offset) / s_scaled.scale))
            unscaled_i = max(unscaled_i, s_scaled.minimum)
            unscaled_i = min(unscaled_i, s_scaled.maximum)
            struct.pack_into(">i", nvm, s_scaled.nvm_word * 4, unscaled_i)
        elif setting.setting_type == asphodel.SETTING_TYPE_FLOAT:
            s_float = setting.u.float_setting
            unscaled_f = (f - s_float.offset) / s_float.scale
            unscaled_f = max(unscaled_f, s_float.minimum)
            unscaled_f = min(unscaled_f, s_float.maximum)
            struct.pack_into(">f", nvm, s_float.nvm_word * 4, unscaled_f)
        else:
            msg = "Setting {} is not a float type".format(setting_index)
            logger.error(msg)

    return nvm
