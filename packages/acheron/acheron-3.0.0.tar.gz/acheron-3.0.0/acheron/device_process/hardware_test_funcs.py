import time

import numpy

import asphodel
from asphodel import (AsphodelNativeDevice, AsphodelStreamInfo,
                      AsphodelChannelInfo, SupplyInfo)
from asphodel.streamutil import stream_fixed_duration
from asphodel.streamutil import filter_channel_data
from asphodel.streamutil import unpack_streaming_data


def supply_test(device: AsphodelNativeDevice, supply_id: int, name: str,
                info: SupplyInfo) -> tuple[bool, str]:

    try:
        value, result_flags = device.check_supply(supply_id)
    except Exception:
        return (False, f"{name} check aborted!")

    scaled_value = value * info.scale + info.offset
    scaled_nominal = info.nominal * info.scale + info.offset
    if scaled_nominal != 0.0:
        percent = (scaled_value) / scaled_nominal * 100.0
    else:
        percent = 0.0
    formatted = asphodel.format_value_ascii(info.unit_type, info.scale,
                                            scaled_value)

    success = True if result_flags == 0 else False
    passfail = "pass" if success else "FAIL"

    message = "{}: {} ({:.0f}%), result=0x{:02x}, {}".format(
        name, formatted, percent, result_flags, passfail)

    return (success, message)


def bridge_test(device: AsphodelNativeDevice, stream_id: int,
                stream: AsphodelStreamInfo, channel_id: int,
                channel: AsphodelChannelInfo) -> tuple[bool, str]:
    channel_name = channel.name.decode("utf-8")

    bridge_count = device.get_strain_bridge_count(channel)

    def get_mean_value(subchannel_index: int) -> tuple[float, str]:
        device_data = stream_fixed_duration(device, stream_ids=[stream_id],
                                            duration=0.1)
        channel_data = filter_channel_data(device_data, stream_id, channel_id)
        _indexes, unpacked_data = unpack_streaming_data(channel_data['data'])
        mean = numpy.nanmean(unpacked_data, axis=0)[subchannel_index]

        decoder = channel_data['channel_decoder']
        subchannel_name = decoder.subchannel_names[subchannel_index]

        return mean, subchannel_name

    try:
        device.warm_up_stream(stream_id, True)

        time.sleep(0.1)

        lines: list[str] = []
        success = True

        try:
            for bridge_index in range(bridge_count):
                subchannel_index = device.get_strain_bridge_subchannel(
                    channel, bridge_index)

                device.set_strain_outputs(channel_id, bridge_index, 1, 0)
                pos_mean, subchannel_name = get_mean_value(subchannel_index)

                device.set_strain_outputs(channel_id, bridge_index, 0, 1)
                neg_mean, _n = get_mean_value(subchannel_index)

                device.set_strain_outputs(channel_id, bridge_index, 0, 0)
                zero_mean, _n = get_mean_value(subchannel_index)

                passed, pos_res, neg_res = device.check_strain_resistances(
                    channel, bridge_index, zero_mean, pos_mean, neg_mean)

                values = device.get_strain_bridge_values(channel, bridge_index)

                if not passed:
                    success = False

                passfail = "pass" if passed else "FAIL"
                s = "{} resistances: pos={} ({:.0%}), neg={} ({:.0%}), {}"
                lines.append(s.format(subchannel_name, round(pos_res),
                                      pos_res / values.nominal, round(neg_res),
                                      neg_res / values.nominal, passfail))
        finally:
            device.warm_up_stream(stream_id, False)
    except Exception:
        return (False, f"{channel_name} bridge check aborted!")

    return (success, "\n".join(lines))


def accel_test(device: AsphodelNativeDevice, stream_id: int,
               stream: AsphodelStreamInfo, channel_id: int,
               channel: AsphodelChannelInfo) -> tuple[bool, str]:
    channel_name = channel.name.decode("utf-8")

    def get_mean_value() -> tuple[float, float, float]:
        # make sure the duration is enough to get at least a couple packets
        duration = max(2 / stream.rate, 0.1)
        device_data = stream_fixed_duration(device, stream_ids=[stream_id],
                                            duration=duration)
        channel_data = filter_channel_data(device_data, stream_id, channel_id)
        _indexes, unpacked_data = unpack_streaming_data(channel_data['data'])
        mean = numpy.nanmean(unpacked_data, axis=0)

        return mean[0:3]  # accel data occupies first 3 indexes

    try:
        device.warm_up_stream(stream_id, True)

        time.sleep(0.1)

        try:
            device.enable_accel_self_test(channel_id, True)
            enabled_mean = get_mean_value()

            device.enable_accel_self_test(channel_id, False)
            disabled_mean = get_mean_value()
        finally:
            device.warm_up_stream(stream_id, False)

        success = device.check_accel_self_test(channel, disabled_mean,
                                               enabled_mean)
    except Exception:
        return (False, f"{channel_name} self test aborted!")

    passfail = "pass" if success else "FAIL"
    return (success, f"{channel_name} self test: {passfail}")
