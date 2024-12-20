from collections import deque

import datetime
import logging
from logging.handlers import QueueHandler
import math
import multiprocessing
from multiprocessing.connection import Connection, wait
import os
import signal
import sys
import threading
import time
from typing import Any, Callable, Optional

import numpy
from numpy.typing import NDArray
import psutil

from asphodel import (AsphodelChannelInfo, AsphodelNativeChannelDecoder,
                      AsphodelNativeDeviceDecoder, AsphodelStreamInfo,
                      StreamRateInfo)
import asphodel
from asphodel.device_info import DeviceInfo
from hyperborea.ringbuffer import RingBuffer

from ..device_logging import DeviceLoggerAdapter
from .types import (CalcControl, CalcData, CalcSettings, ChannelInformation,
                    LimitType, Trigger)

logger = logging.getLogger(__name__)


class CalcDataProcessor:

    def __init__(self, decoder: AsphodelNativeDeviceDecoder,
                 channel_info: dict[int, ChannelInformation],
                 data_pipe: Connection, logger: DeviceLoggerAdapter,
                 is_shown: bool, channel_interval: float, plot_interval: float,
                 fft_interval: float, triggers: set[Trigger]):
        self.device_decoder = decoder
        self.channel_info = channel_info
        self.data_pipe = data_pipe
        self.logger = logger
        self.is_shown = is_shown
        self.channel_interval = channel_interval
        self.plot_interval = plot_interval
        self.fft_interval = fft_interval

        self.current_channel_id: Optional[int] = None
        self.current_subchannel_index: Optional[int] = None

        self.mean_ringbuffers: dict[int, RingBuffer] = {}
        self.plot_ringbuffers: dict[int, RingBuffer] = {}
        self.fft_ringbuffers: dict[int, RingBuffer] = {}

        self.connectivity_pipe: Optional[Connection] = None
        self.connectivity_deques: dict[int, deque[NDArray[numpy.float64]]] = {}

        self.data_lock = threading.Lock()  # for locking self.data_pipe

        self.trigger_lock = threading.Lock()
        self.triggers_by_channel: dict[int, set[Trigger]] = {}
        self.active_triggers: set[str] = set()
        self.change_triggers(triggers)  # easiest way to init the triggers

        self.lost_packet_lock = threading.Lock()
        self.lost_packet_count = 0
        self.lost_packet_last_time: Optional[datetime.datetime] = None
        self.recent_lost_packet_count = 0
        self.lost_packet_deque: deque[tuple[datetime.datetime, int]] = deque()
        self.last_lost_packet_update: Optional[tuple] = None

        self.stopped = threading.Event()

        self.setup_decoder()

        self.update_thread = threading.Thread(target=self.update_thread_run)
        self.update_thread.start()

    def stop_and_join(self) -> None:
        self.stopped.set()
        self.update_thread.join()

        if self.connectivity_pipe is not None:
            try:
                self.connectivity_pipe.send(None)
                self.connectivity_pipe.close()
                self.connectivity_pipe = None
            except Exception:
                pass  # can't do anything about it now

        self.connectivity_deques.clear()

    def set_connectivity_pipe(self, pipe: Connection) -> None:
        self.connectivity_pipe = pipe

    def process_connectivity(self) -> None:
        if self.connectivity_pipe is not None:
            messages: list[tuple[int, NDArray[numpy.float64]]] = []
            for channel_id, d in self.connectivity_deques.items():
                values: list[NDArray[numpy.float64]] = []
                while d:
                    values.append(d.popleft())
                if values:
                    messages.append((channel_id, numpy.concatenate(values)))
            self.connectivity_pipe.send(messages)

    def setup_decoder(self) -> None:
        self.device_decoder.set_unknown_id_callback(self.unknown_id_cb)

        channel_decoders: dict[int, AsphodelNativeChannelDecoder] = {}
        for i, stream_decoder in enumerate(self.device_decoder.decoders):
            stream_id = self.device_decoder.stream_ids[i]
            lost_packet_cb = self.create_lost_packet_callback(stream_id)
            stream_decoder.set_lost_packet_callback(lost_packet_cb)
            for j, channel_decoder in enumerate(stream_decoder.decoders):
                channel_id = stream_decoder.stream_info.channel_index_list[j]
                channel_decoders[channel_id] = channel_decoder

        # operate on the channel decoders sorted by channel id
        for channel_id in sorted(channel_decoders.keys()):
            channel_decoder = channel_decoders[channel_id]
            self.setup_channel(channel_id, channel_decoder)

    def setup_channel(self, channel_id: int,
                      channel_decoder: AsphodelNativeChannelDecoder) -> None:
        channel_info = self.channel_info[channel_id]

        mean_rb = RingBuffer(channel_info.mean_len,
                             channel_decoder.subchannels)
        self.mean_ringbuffers[channel_id] = mean_rb
        plot_rb = RingBuffer(channel_info.plot_len,
                             channel_decoder.subchannels)
        self.plot_ringbuffers[channel_id] = plot_rb
        fft_rb = RingBuffer(channel_info.fft_sample_len,
                            channel_decoder.subchannels)
        self.fft_ringbuffers[channel_id] = fft_rb

        downsample = channel_info.downsample_factor != 1

        def callback(_counter: int, data: list[float], samples: int,
                     subchannels: int) -> None:
            d = numpy.array(data, dtype=numpy.float64).reshape(
                (samples, subchannels))
            if downsample:
                plot_rb.append(d[-1, :])
            else:
                plot_rb.extend(d)
            fft_rb.extend(d)
            mean_rb.extend(d)

            if self.connectivity_pipe is not None:
                connectivity_deque = self.connectivity_deques.get(channel_id)
                if connectivity_deque is None:
                    connectivity_deque = deque()
                    self.connectivity_deques[channel_id] = connectivity_deque
                connectivity_deque.append(d)

        channel_decoder.set_callback(callback)

    def create_lost_packet_callback(
            self, stream_id: int) -> Callable[[int, int], None]:

        def lost_packet_callback(current: int, last: int) -> None:
            if last == 0xFFFFFFFFFFFFFFFF:
                # restarted streaming in the middle
                return

            lost = (current - last - 1) & 0xFFFFFFFFFFFFFFFF

            now = datetime.datetime.now(datetime.timezone.utc)

            with self.lost_packet_lock:
                self.lost_packet_count += lost
                self.recent_lost_packet_count += lost
                self.lost_packet_last_time = now

            self.lost_packet_deque.append((now, lost))

            for channel_id, channel_info in self.channel_info.items():
                if channel_info.stream_id == stream_id:
                    fft_ringbuffer = self.fft_ringbuffers[channel_id]
                    fft_ringbuffer.clear()

        return lost_packet_callback

    def update_lost_packets(self) -> None:
        lost_count_too_old = 0
        now = datetime.datetime.now(datetime.timezone.utc)
        twenty_secs_ago = now - datetime.timedelta(seconds=20)
        while len(self.lost_packet_deque):
            lost_dt, lost = self.lost_packet_deque[0]
            if lost_dt < twenty_secs_ago:
                lost_count_too_old += lost
                self.lost_packet_deque.popleft()
            else:
                break

        with self.lost_packet_lock:
            self.recent_lost_packet_count -= lost_count_too_old
            if self.recent_lost_packet_count < 0:
                self.recent_lost_packet_count = 0

            # grab local copies
            total = self.lost_packet_count
            recent = self.recent_lost_packet_count
            last_datetime = self.lost_packet_last_time

        update = (CalcData.LOST_PACKET_UPDATE, total, last_datetime, recent)
        if self.last_lost_packet_update != update:
            self.last_lost_packet_update = update
            with self.data_lock:
                self.data_pipe.send(update)

    def get_stream_rate(self, rate_info: StreamRateInfo) -> Optional[float]:
        if rate_info.available:
            rate_channel_id = rate_info.channel_index
            ringbuffer = self.fft_ringbuffers[rate_channel_id]
            if len(ringbuffer) != 0:
                rate_data = ringbuffer.get_contents()
                raw_rate: float = numpy.average(rate_data)  # type: ignore

                if not math.isfinite(raw_rate):
                    return None

                # compute channel rate
                stream_rate = raw_rate * rate_info.scale + rate_info.offset
                if rate_info.invert:
                    if stream_rate != 0.0:
                        stream_rate = 1 / stream_rate
                    else:
                        stream_rate = 0.0  # no divide by zero please

                # no formatter is being applied to channels, so nothing to do

                return stream_rate
            else:
                # no data available to compute rate yet
                return None
        else:
            return None

    def change_triggers(self, triggers: set[Trigger]) -> None:
        triggers_by_channel: dict[int, set[Trigger]] = {}
        for trigger in triggers:
            channel_triggers = triggers_by_channel.get(trigger.channel_id)
            if channel_triggers:
                channel_triggers.add(trigger)
            else:
                triggers_by_channel[trigger.channel_id] = set((trigger,))

        available_ids = set(trigger.id for trigger in triggers)

        with self.trigger_lock:
            self.triggers_by_channel = triggers_by_channel
            active_count = len(self.active_triggers)
            self.active_triggers.intersection_update(available_ids)
            if len(self.active_triggers) != active_count:
                # some active triggers were removed
                with self.data_lock:
                    self.data_pipe.send(
                        (CalcData.ACTIVE_TRIGGERS_CHANGED,
                         self.active_triggers))

    def check_triggers(self, triggers: set[Trigger],
                       mean: NDArray[numpy.float64],
                       std: NDArray[numpy.float64]) -> None:
        for trigger in triggers:
            was_active = trigger.id in self.active_triggers

            if trigger.subchannel_index >= len(mean):
                # out of bounds: ignore
                # NOTE: mean and std are the same length
                continue

            if trigger.limit_type == LimitType.MEAN_HIGH_LIMIT:
                value = mean[trigger.subchannel_index]
                if was_active:
                    active = value >= trigger.deactivate_limit
                else:
                    active = value > trigger.activate_limit
            elif trigger.limit_type == LimitType.MEAN_LOW_LIMIT:
                value = mean[trigger.subchannel_index]
                if was_active:
                    active = value <= trigger.deactivate_limit
                else:
                    active = value < trigger.activate_limit
            elif trigger.limit_type == LimitType.STD_HIGH_LIMIT:
                value = std[trigger.subchannel_index]
                if was_active:
                    active = value >= trigger.deactivate_limit
                else:
                    active = value > trigger.activate_limit
            else:  # trigger.limit_type == LimitType.STD_LOW_LIMIT
                value = std[trigger.subchannel_index]
                if was_active:
                    active = value <= trigger.deactivate_limit
                else:
                    active = value < trigger.activate_limit

            if active and not was_active:
                self.active_triggers.add(trigger.id)
                self.triggers_changed = True
            elif not active and was_active:
                self.active_triggers.remove(trigger.id)
                self.triggers_changed = True

    def update_channels(self) -> None:
        with self.trigger_lock:
            self.triggers_changed = False
            for channel_id, ringbuffer in self.mean_ringbuffers.items():
                if ringbuffer is not None and len(ringbuffer) > 0:
                    d = ringbuffer.get_contents()
                    mean: NDArray[numpy.float64] = numpy.mean(d, axis=0)
                    std: NDArray[numpy.float64] = numpy.std(d, axis=0)

                    with self.data_lock:
                        self.data_pipe.send(
                            (CalcData.CHANNEL_UPDATE, channel_id, mean, std))

                    channel_triggers = self.triggers_by_channel.get(channel_id)
                    if channel_triggers:
                        self.check_triggers(channel_triggers, mean, std)
            if self.triggers_changed:
                with self.data_lock:
                    self.data_pipe.send(
                        (CalcData.ACTIVE_TRIGGERS_CHANGED,
                         self.active_triggers))

    def update_plots(self) -> None:
        if not self.is_shown:
            return

        channel_id = self.current_channel_id
        if channel_id is None:
            return

        channel_info = self.channel_info[channel_id]

        stream_rate = self.get_stream_rate(channel_info.rate_info)
        if not stream_rate:
            channel_rate = channel_info.rate
        else:
            channel_rate = stream_rate * channel_info.samples
        plot_rate = channel_rate / channel_info.downsample_factor

        plot_array = self.plot_ringbuffers[channel_id].get_contents()
        if len(plot_array) > 0:
            length = len(plot_array)
            start = -(length - 1) / plot_rate
            time_axis = numpy.linspace(start, 0, length)
            with self.data_lock:
                self.data_pipe.send(
                    (CalcData.PLOT_UPDATE, channel_id, time_axis, plot_array))

    def update_ffts(self) -> None:
        if not self.is_shown:
            return

        channel_id = self.current_channel_id
        if channel_id is None:
            return

        subchannel_index = self.current_subchannel_index
        if subchannel_index is None:
            return

        channel_info = self.channel_info[channel_id]

        stream_rate = self.get_stream_rate(channel_info.rate_info)
        if not stream_rate:
            fft_freq_axis = channel_info.fft_freq_axis
        else:
            channel_rate = stream_rate * channel_info.samples
            fft_freq_axis = numpy.fft.rfftfreq(channel_info.fft_size,
                                               1 / channel_rate)

        ringbuffer = self.fft_ringbuffers[channel_id]
        fft_array = ringbuffer.get_contents()
        if ringbuffer.maxlen != len(fft_array):
            buffering_progress = len(fft_array) / ringbuffer.maxlen
            with self.data_lock:
                self.data_pipe.send(
                    (CalcData.FFT_UPDATE, channel_id, subchannel_index,
                     fft_freq_axis, buffering_progress))
        else:
            fft_array = fft_array[:, subchannel_index].flatten()
            fft_array -= numpy.mean(fft_array)
            fft_size = channel_info.fft_size
            fft_array = fft_array[0:fft_size]
            fft_data = numpy.abs(numpy.fft.rfft(fft_array)) * 2 / fft_size
            with self.data_lock:
                self.data_pipe.send(
                    (CalcData.FFT_UPDATE, channel_id, subchannel_index,
                     fft_freq_axis, fft_data))

    def set_is_shown(self, is_shown: bool) -> None:
        self.is_shown = is_shown
        if is_shown:
            # update the plots now
            self.update_plots()
            self.update_ffts()

    def plot_change(self, channel_id: Optional[int],
                    subchannel_index: Optional[int]) -> None:
        if channel_id == -1:
            channel_id = None
        if subchannel_index == -1:
            subchannel_index = None

        self.current_channel_id = channel_id
        self.current_subchannel_index = subchannel_index

    def reset_lost_packets(self) -> None:
        self.lost_packet_deque.clear()
        with self.lost_packet_lock:
            self.recent_lost_packet_count = 0

    def unknown_id_cb(self, unknown_id: int) -> None:
        with self.data_lock:
            self.data_pipe.send((CalcData.UNKNOWN_ID, unknown_id))

    def update_thread_run(self) -> None:
        update_funcs: list[tuple[Callable, float]] = []

        if self.fft_interval:
            update_funcs.append((self.update_ffts, self.fft_interval))

        if self.plot_interval:
            update_funcs.append((self.update_plots, self.plot_interval))

        if self.channel_interval:
            update_funcs.append((self.update_channels, self.channel_interval))
            update_funcs.append(
                (self.update_lost_packets, self.channel_interval))

        if not update_funcs:
            # nothing to update
            return

        next_run = [time.monotonic()] * len(update_funcs)

        try:
            while True:
                now = time.monotonic()
                for i, (func, interval) in enumerate(update_funcs):
                    if next_run[i] <= now:
                        func()
                        next_run[i] += interval
                        if next_run[i] <= now:
                            # fell behind, just wait for the interval to pass
                            next_run[i] = now + interval

                wait_time = min(next_run) - time.monotonic()
                if wait_time < 0.0:
                    wait_time = 0.0
                if self.stopped.wait(wait_time):
                    # all done
                    self.logger.debug("Calc process update thread stopped")
                    return
        except Exception:
            self.logger.exception("Unhandled exception in update_thread_run")


class CalcRunner:

    def __init__(self, packet_pipe: Connection, data_pipe: Connection,
                 ctrl_pipe: Connection, serial_number: str, is_shown: bool,
                 settings: CalcSettings, triggers: set[Trigger]):
        self.packet_pipe = packet_pipe
        self.data_pipe = data_pipe
        self.ctrl_pipe = ctrl_pipe
        self.serial_number = serial_number
        self.is_shown = is_shown
        self.settings = settings
        self.triggers = triggers

        self.logger = DeviceLoggerAdapter(logger, self.serial_number)

        self.decoder: Optional[AsphodelNativeDeviceDecoder] = None
        self.data_processor: Optional[CalcDataProcessor] = None
        self.device_info: DeviceInfo
        self.active_streams: frozenset[int]

    def create_decoder(
        self, device_info: DeviceInfo, active_streams: frozenset[int]
    ) -> tuple[AsphodelNativeDeviceDecoder, dict[int, ChannelInformation]]:
        channel_info: dict[int, ChannelInformation] = {}

        streams = device_info.streams
        channels = device_info.channels

        info_list = []
        for i, stream in enumerate(streams):
            if i not in active_streams:
                continue
            channel_info_list = []
            ids: list[int] = stream.channel_index_list[0:stream.channel_count]
            for channel_id in ids:
                channel_info_list.append(channels[channel_id])
            info_list.append((i, stream, channel_info_list))

        device_decoder = asphodel.nativelib.create_device_decoder(
            info_list, device_info.stream_filler_bits,
            device_info.stream_id_bits)

        for i, stream_decoder in enumerate(device_decoder.decoders):
            stream_id: int = device_decoder.stream_ids[i]
            for j, channel_decoder in enumerate(stream_decoder.decoders):
                channel_id = stream_decoder.stream_info.channel_index_list[j]
                channel = channels[channel_id]
                channel_info[channel_id] = self.create_channel_info(
                    device_info, stream_id, streams[stream_id], channel_id,
                    channel, channel_decoder)

        return device_decoder, channel_info

    def create_channel_info(self, device_info: DeviceInfo, stream_id: int,
                            stream: AsphodelStreamInfo, channel_id: int,
                            channel: AsphodelChannelInfo,
                            channel_decoder: AsphodelNativeChannelDecoder)\
            -> ChannelInformation:
        rate_info = device_info.stream_rate_info[stream_id]
        samples: int = channel.samples  # type: ignore
        channel_rate = samples * stream.rate

        # figure out how much data to collect
        sample_len = math.ceil(10.0 * channel_rate)  # 10 seconds
        # round up to next power of 2 (for faster FFT)
        sample_len = 2**(math.ceil(math.log2(sample_len)))

        if self.settings.downsample and sample_len > 32768:
            downsample_factor = samples
        else:
            downsample_factor = 1

        fft_sample_len = min(sample_len, 32768)

        return ChannelInformation(
            name=channel_decoder.channel_name,
            channel_id=channel_id,
            stream_id=stream_id,
            channel=channel,
            subchannel_names=channel_decoder.subchannel_names,
            rate_info=rate_info,
            samples=samples,
            rate=channel_rate,
            downsample_factor=downsample_factor,
            mean_len=math.ceil(1.0 * channel_rate),  # 1 second
            plot_len=sample_len // downsample_factor,
            fft_shortened=(fft_sample_len != sample_len),
            fft_sample_len=fft_sample_len,
            fft_freq_axis=numpy.fft.rfftfreq(fft_sample_len, 1 / channel_rate),
            fft_size=fft_sample_len,
        )

    def stop_processing(self) -> None:
        self.decoder = None
        if self.data_processor:
            self.data_processor.stop_and_join()
            self.data_processor = None

    def start_processing(self) -> None:
        self.stop_processing()

        self.decoder, channel_info = self.create_decoder(
            self.device_info, self.active_streams)
        self.data_pipe.send((CalcData.PROCESSING_START, self.device_info,
                             self.active_streams, channel_info))
        self.data_processor = CalcDataProcessor(
            self.decoder, channel_info, self.data_pipe, self.logger,
            self.is_shown, self.settings.channel_interval,
            self.settings.plot_interval, self.settings.fft_interval,
            self.triggers)

    def run(self) -> None:
        running = True

        try:
            self.logger.debug("Calc process started")

            me = psutil.Process(os.getpid())
            object_list = [self.packet_pipe, self.ctrl_pipe]
            while True:
                parent = me.parent()
                if parent is None or not parent.is_running():
                    break

                ready_pipes: list[Connection] = wait(
                    object_list, timeout=0.1)  # type: ignore
                for pipe in ready_pipes:
                    if pipe == self.packet_pipe:
                        message = pipe.recv()
                        if running:
                            if message is None:
                                self.stop_processing()
                                self.data_pipe.send(
                                    (CalcData.PROCESSING_STOP,))
                            elif type(message) is tuple:
                                self.device_info, self.active_streams = message
                                self.start_processing()
                            else:
                                if self.decoder and self.data_processor:
                                    for packet in message:
                                        self.decoder.decode(packet)
                                    self.data_processor.process_connectivity()
                    else:
                        ctrl = pipe.recv()
                        if ctrl[0] == CalcControl.STOP:
                            running = False
                            self.stop_processing()
                        elif ctrl[0] == CalcControl.CLOSE:
                            # all done!
                            return
                        elif ctrl[0] == CalcControl.SET_SHOWN:
                            self.is_shown = ctrl[1]
                            if self.data_processor:
                                self.data_processor.set_is_shown(ctrl[1])
                        elif ctrl[0] == CalcControl.PLOT_CHANGE:
                            if self.data_processor:
                                self.data_processor.plot_change(*ctrl[1:])
                        elif ctrl[0] == CalcControl.RESET_LOST_PACKETS:
                            if self.data_processor:
                                self.data_processor.reset_lost_packets()
                        elif ctrl[0] == CalcControl.CHANGE_SETTINGS:
                            self.settings = ctrl[1]
                            if self.decoder:
                                self.start_processing()
                        elif ctrl[0] == CalcControl.CHANGE_TRIGGERS:
                            triggers: set[Trigger] = ctrl[1]
                            self.triggers = triggers
                            if self.data_processor:
                                self.data_processor.change_triggers(triggers)
                        elif ctrl[0] == CalcControl.SET_CONNECTIVITY_PIPE:
                            connectivity_pipe: Connection = ctrl[1]
                            if self.data_processor:
                                self.data_processor.set_connectivity_pipe(
                                    connectivity_pipe)
        except Exception:
            self.logger.exception("Unhandled exception in calc process run")
        finally:
            self.stop_processing()
            self.logger.debug("Calc process exiting")


def run_calc_runner(log_queue: multiprocessing.Queue, *args: Any,
                    **kwargs: Any) -> None:
    # fix a bug with stderr and stdout being None
    sys.stdout = open(os.devnull)
    sys.stderr = open(os.devnull)

    handler = QueueHandler(log_queue)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

    # ctrl+c handling: want to let the main process send the exit command
    if sys.platform == "win32":
        # the best way on windows? since we can't create a new process group
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    else:
        # move to a new process group (won't be signalled with ctrl+c)
        os.setpgrp()

    try:
        calc_runner = CalcRunner(*args, **kwargs)
        calc_runner.run()
    except Exception:
        logger.exception("unhandled exception in run_calc_runner")
    finally:
        log_queue.close()
        log_queue.join_thread()
