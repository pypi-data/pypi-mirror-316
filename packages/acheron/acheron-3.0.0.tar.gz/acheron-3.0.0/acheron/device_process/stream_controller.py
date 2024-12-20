from collections import deque
from dataclasses import dataclass
import datetime
import enum
import functools
import logging
import multiprocessing.connection
import platform
from queue import Empty, Queue
import threading
import time
from typing import Any, Callable, cast, Iterable, Optional, Protocol, Union
import weakref

from diskcache import Cache

import asphodel
from asphodel.device_info import (DeviceInfo, get_active_scan_info,
                                  get_device_info, get_remote_board_info)
from asphodel.device_info import logger as device_info_logger

from . import proxy_remote
from .bootloader import do_bootload
from .rgb_manager import RGBManager
from .schedule import (get_compatible_set, OutputConfig, RemoteSchedule,
                       Schedule, ScheduleItem)
from .writer import StreamWriter

logger = logging.getLogger(__name__)


instances: dict[asphodel.AsphodelNativeDevice, "StreamController"] = {}


def start_stream_controller(device: asphodel.AsphodelNativeDevice,
                            *args: Any, **kwargs: Any) -> None:
    device_logger = proxy_remote.get_device_logger(logger, device)
    device_logger.debug("Starting streaming instance")

    if device in instances:
        stop_stream_controller(device)

    device_lock = proxy_remote.device_lock

    instance = StreamController(device, device_lock, device_logger, *args,
                                **kwargs)
    instances[device] = instance
    instance.start()

    proxy_remote.register_device_cleanup(device, stop_stream_controller)
    proxy_remote.register_device_cleanup(
        device, join_streaming, weakref.ref(instance), device_logger)


def stop_stream_controller(device: asphodel.AsphodelNativeDevice) -> None:
    if device not in instances:
        return

    instances[device].stop()

    device_logger = proxy_remote.get_device_logger(logger, device)
    device_logger.debug("Stopped streaming instance")

    del instances[device]

    proxy_remote.unregister_device_cleanup(device, stop_stream_controller)


def join_streaming(device: asphodel.AsphodelNativeDevice,
                   instance_weakref: weakref.ref["StreamController"],
                   device_logger: proxy_remote.DeviceLoggerAdapter) -> None:
    # called during cleanup, on proxy exit

    instance = instance_weakref()
    if instance:
        device_logger.debug("Waiting for streaming instance to finish")
        instance.join()
        device_logger.debug("Finished streaming instance")
    else:
        device_logger.debug("Streaming instance already garbage collected")

    proxy_remote.unregister_device_cleanup(
        device, join_streaming, instance_weakref, device_logger)


@dataclass()
class ScanResult:
    serial_number: int
    last_seen: datetime.datetime
    bootloader: bool
    asphodel_type: int
    device_mode: int
    scan_strength: Optional[int]
    board_info: Optional[tuple[str, int]]


@dataclass(frozen=True)
class RemoteInfo:
    serial_number: int
    bootloader: bool


class RemoteWrapper:
    def __init__(self, remote: asphodel.AsphodelNativeDevice,
                 stream_controller: "StreamController",
                 remote_info: RemoteInfo) -> None:
        self.remote: Optional[asphodel.AsphodelNativeDevice] = remote
        self.stream_controller = stream_controller
        self.remote_info = remote_info

    def __getattr__(self, name: str) -> Any:
        if self.remote is None:
            raise asphodel.AsphodelError("Remote Wrapper Closed")
        return getattr(self.remote, name)

    def close(self) -> None:
        pass  # ignore this call


def create_remote(device: asphodel.AsphodelNativeDevice, serial_number: int,
                  bootloader: bool) -> RemoteWrapper:
    return instances[device].get_remote(serial_number, bootloader)


@dataclass()
class StreamSettings:
    auto_rgb: bool
    response_time: int
    buffer_time: int
    timeout: int
    default_output_config: OutputConfig


@dataclass()
class RFFixedTestParams:
    channel: int
    duration: int
    mode: int


@dataclass()
class RFSweepTestParams:
    start: int
    stop: int
    hop_interval: int
    hop_count: int
    mode: int


@dataclass()
class RFTestParams:
    test_params: Union[RFFixedTestParams, RFSweepTestParams]
    finished_pipe: multiprocessing.connection.Connection


@enum.unique
class StreamControl(enum.Enum):
    CHANGE_SETTINGS = enum.auto()
    UPDATE_SCHEDULE_ITEM = enum.auto()
    DELETE_SCHEDULE_IDS = enum.auto()
    SET_RGB = enum.auto()
    GET_RGB_STATE = enum.auto()
    SET_LED = enum.auto()
    SET_CTRL_VAR = enum.auto()
    SET_DEVICE_MODE = enum.auto()
    SET_RF_POWER = enum.auto()
    WRITE_NVM = enum.auto()
    FORCE_RESET = enum.auto()
    FORCE_RUN_BOOTLOADER = enum.auto()
    FORCE_RUN_APPLICATION = enum.auto()
    DO_BOOTLOADER = enum.auto()
    DO_HARDWARE_TESTS = enum.auto()
    DO_RF_TEST = enum.auto()
    DO_ACTIVE_SCAN = enum.auto()
    DO_RADIO_FUNCTION = enum.auto()
    ACTIVE_TRIGGERS_CHANGED = enum.auto()
    _REMOTE_INFO = enum.auto()  # NOTE: internal use only
    _REMOTE_CLOSED = enum.auto()  # NOTE: internal use only
    _WAKEUP = enum.auto()  # NOTE: internal use only


@enum.unique
class StreamStatus(enum.Enum):
    RECONNECTING = enum.auto()  # ()
    DEVICE_INFO_START = enum.auto()  # ()
    DEVICE_INFO_PROGRESS = enum.auto()  # (finished, total, section_name)
    WRITE_NVM_PROGRESS = enum.auto()  # (finished, total)
    DEVICE_INFO_READY = enum.auto()  # (device_info,)
    STREAMING_STARTED = enum.auto()  # (active_streams,)
    STREAMING_ERROR_TIMEOUT = enum.auto()  # ()
    STREAMING_ERROR_DISCONNECT = enum.auto()  # ()
    STREAMING_ERROR_OTHER = enum.auto()  # (err_id)
    BOOTLOADER_PROGRESS = enum.auto()  # (finished, total, status_str)
    BOOTLOADER_FINISHED = enum.auto()  # (success, event_data)
    DISCONNECTED = enum.auto()  # ()
    RGB_UPDATE = enum.auto()  # (index, values)
    DEVICE_MODE_UPDATE = enum.auto()  # (success, mode)
    STARTED_FILE = enum.auto()  # (file_path, schedule_id, marked_for_upload)
    FINISHED_FILE = enum.auto()  # (file_path, schedule_id, marked_for_upload)
    ONGOING_ITEMS = enum.auto()  # (running_ids, rf_power_needed, schedule_len)
    FINISHED_ITEM = enum.auto()  # (schedule_id, success)
    HARDWARE_TEST_FUNCTION_FINISHED = enum.auto()  # (run_id, test_id, data)
    HARDWARE_TEST_RUN_FINISHED = enum.auto()  # (run_id)
    RF_TEST_FINISHED = enum.auto()  # ()
    REMOTE_CONNECTING = enum.auto()  # (serial_number_int, bootloader)
    REMOTE_CONNECTED = enum.auto()  # (serial_int, serial_str, bootloader)
    REMOTE_DISCONNECTED = enum.auto()  # ()
    SCAN_DATA = enum.auto()  # (list of ScanResult)
    ACTIVE_SCAN_DATA = enum.auto()  # (serial, active_scan | None)
    SCAN_FIRST_PASS = enum.auto()  # ()
    RADIO_FUNCTION_FINISHED = enum.auto()  # (ran, result)


class Joinable(Protocol):
    def join(self) -> None:
        ...


HardwareTestFunction = Callable[[asphodel.AsphodelNativeDevice], Any]


class StreamController:
    def __init__(self, device: asphodel.AsphodelNativeDevice,
                 device_lock: threading.Lock, logger: logging.LoggerAdapter,
                 settings: StreamSettings,
                 schedule_items: Iterable[ScheduleItem], main_schedule_id: str,
                 active_triggers: frozenset[str], diskcache: Cache,
                 ctrl_pipe: multiprocessing.connection.Connection,
                 packet_pipe: multiprocessing.connection.Connection,
                 status_pipe: multiprocessing.connection.Connection):
        self.device = device
        self.device_lock = device_lock
        self.logger = logger
        self.settings = settings
        self.main_schedule_id = main_schedule_id
        self.diskcache = diskcache
        self.ctrl_pipe = ctrl_pipe
        self.packet_pipe = packet_pipe

        # set the device error callback for logging purposes
        self.device.set_error_callback(self._device_error_callback)

        self.device_info_logger = proxy_remote.get_device_logger(
            device_info_logger, device)

        self.rgb_manager = RGBManager(device, settings.auto_rgb,
                                      self._rgb_callback)

        self.schedule: Union[Schedule, RemoteSchedule]
        self.parent_controller: Optional["StreamController"]
        try:
            controller: "StreamController" = \
                self.device.stream_controller  # type: ignore
            self.parent_controller = controller
            remote_info: RemoteInfo = self.device.remote_info  # type: ignore
            self.parent_controller.register_subcontroller_locked(self)
            self.schedule = self.parent_controller.get_remote_schedule(
                schedule_items, remote_info)
        except AttributeError:
            self.parent_controller = None
            self.schedule = Schedule(schedule_items, active_triggers)

        self.ctrl_queue: Queue[tuple[Any, ...]] = Queue()

        self.status_pipe_lock = threading.Lock()
        self.status_pipe = status_pipe

        self.finished = threading.Event()
        self.disconnected = threading.Event()

        self.reset_function: Optional[Callable] = None
        self.hw_tests: Optional[tuple[list[tuple[HardwareTestFunction, str]],
                                      str]] = None
        self.rf_test_params: Optional[RFTestParams] = None

        self.remote_wrapper: Optional[RemoteWrapper] = None
        self.subcontroller: Optional["StreamController"] = None

        self.poll_thread = threading.Thread(target=self.poll_thread_run)
        self.stream_thread = threading.Thread(target=self.stream_thread_run)
        self.packet_thread: Optional[threading.Thread] = None
        self.check_connection_thread: Optional[threading.Thread] = None
        self.radio_thread: Optional[threading.Thread] = None
        self.rf_power_thread: Optional[threading.Thread] = None

        self.radio_queue: Queue[tuple[Any, ...]] = Queue()

        self.writer_lock = threading.Lock()
        self.writers: dict[str, StreamWriter] = {}

        self.stop_lock = threading.Lock()
        self.stop_called = False
        self.stop_finished = threading.Event()
        self.background_join_deque: deque[Joinable] = deque()
        self.background_join_thread = threading.Thread(
            target=self.background_join_run)
        self.background_join_thread.start()

    def start(self) -> None:
        self.poll_thread.start()
        self.stream_thread.start()

    def stop(self) -> None:  # NOTE: must be called with the device lock held!
        # NOTE: this function may be called multiple times
        # (even in parallel because of the device lock release call)

        # must release the device lock before acquiring the stop lock
        self.device_lock.release()

        reacquired = False

        with self.stop_lock:
            if not self.stop_called:
                self.stop_called = True
                self.finished.set()

                try:
                    # signal stream_thread to stop
                    self.ctrl_queue.put((StreamControl._WAKEUP,))

                    # NOTE: must not hold device lock while waiting for the
                    # stream thread to finish
                    self.stream_thread.join()
                except Exception:
                    self.logger.exception(
                        "Error stopping stream thread in stop()")
                finally:
                    # reacquire now
                    self.device_lock.acquire()
                    reacquired = True

                try:
                    # this is probably redundant, as stream_thread should call
                    # it on exit. Still, it won't take long!
                    self.stop_all_writers()
                except Exception:
                    self.logger.exception(
                        "Error stopping writers in stop()")

                # this is a bit hacky, but I don't know a better way to deal
                # with this
                try:
                    self.schedule.delete_item_id(self.main_schedule_id)
                    if self.parent_controller:
                        self.parent_controller.schedule_changed()
                        self.parent_controller.unregister_subcontroller_locked(
                            self)
                        self.parent_controller = None
                except Exception:
                    self.logger.exception("Error updating schedule in stop()")

                with self.status_pipe_lock:
                    try:
                        self.status_pipe.send((StreamStatus.DISCONNECTED,))
                    except BrokenPipeError:
                        pass  # pipe already closed: ignore
                    except Exception:
                        self.logger.exception(
                            "Error writing to status pipe in stop()")

                try:
                    self.poll_thread.join()
                except Exception:
                    self.logger.exception(
                        "Error joining poll thread in stop()")

                try:
                    self.packet_pipe.close()
                except Exception:
                    self.logger.exception(
                        "Error closing packet pipe in stop()")

                # signal to the background join thread nothing more will be
                # added to the deque, which will close status_pipe when done
                self.stop_finished.set()

        if not reacquired:
            # must reacquire before exiting
            self.device_lock.acquire()

    def join(self) -> None:
        if not self.stop_finished.is_set():
            self.stop()

        self.device_lock.release()
        self.background_join_thread.join()
        self.device_lock.acquire()

    def _do_join_pass(self) -> None:
        while self.background_join_deque:
            item = self.background_join_deque.popleft()
            try:
                item.join()
            except Exception:
                self.logger.exception("Failed to join %s", item)

    def background_join_run(self) -> None:
        try:
            while not self.stop_finished.wait(timeout=0.1):
                self._do_join_pass()

            # do one final pass
            self._do_join_pass()
        except Exception:
            self.logger.exception("Uncaught exception in background_join_run")
        finally:
            # no need for a lock, nothing else can be using it at this point
            try:
                self.status_pipe.send(None)  # final transmission
            except BrokenPipeError:
                pass  # pipe already closed: ignore
            self.status_pipe.close()

    def poll_thread_run(self) -> None:
        try:
            while not self.finished.is_set():
                ready = self.ctrl_pipe.poll(0.1)
                if ready:
                    try:
                        message = self.ctrl_pipe.recv()
                        self.ctrl_queue.put(message)
                    except EOFError:
                        return
        except Exception:
            self.logger.exception("Uncaught exception in poll_thread_run")
        finally:
            self.ctrl_pipe.close()

    def _device_error_callback(self, _device: asphodel.AsphodelNativeDevice,
                               error_code: int) -> None:
        error_name = asphodel.asphodel_error_name(error_code)
        self.logger.error("Device error code %s: %s", error_code, error_name)

    def schedule_changed(self) -> None:
        self.ctrl_queue.put((StreamControl._WAKEUP,))

    def writer_file_started(self, filename: str, schedule_id: str,
                            marked_for_upload: bool) -> None:
        with self.status_pipe_lock:
            self.status_pipe.send((StreamStatus.STARTED_FILE, filename,
                                   schedule_id, marked_for_upload))

    def writer_file_finished(self, filename: str, schedule_id: str,
                             marked_for_upload: bool) -> None:
        try:
            with self.status_pipe_lock:
                self.status_pipe.send((StreamStatus.FINISHED_FILE, filename,
                                       schedule_id, marked_for_upload))
        except BrokenPipeError:
            pass  # pipe already closed: ignore

    def writer_stopped(self, schedule_id: str, success: bool) -> None:
        with self.writer_lock:
            try:
                writer = self.writers.pop(schedule_id)
                writer.close()
                self.background_join_deque.append(writer)
                self.logger.debug("Writer stopped for %s", schedule_id)
            except KeyError:
                pass

        self.schedule.delete_item_id(schedule_id)

        # let everyone know
        self.schedule_changed()
        if self.parent_controller:
            self.parent_controller.schedule_changed()
        if self.subcontroller:
            self.subcontroller.schedule_changed()

        if not success:
            self.logger.info("Failure on schedule item %s", schedule_id)

        with self.status_pipe_lock:
            self.status_pipe.send((StreamStatus.FINISHED_ITEM, schedule_id,
                                   success))

    def stop_all_writers(self) -> None:
        with self.writer_lock:
            for writer in self.writers.values():
                writer.close()
                self.background_join_deque.append(writer)
            self.writers.clear()

    def start_writers(self, device_info: DeviceInfo, extra_info: dict,
                      schedule_items: set[ScheduleItem]) -> None:
        rf_power_needed = any(s.needs_rf_power for s in schedule_items)
        schedule_ids_set: set[str] = set()
        for schedule_item in schedule_items:
            schedule_ids_set.add(schedule_item.id)
            if schedule_item.output_config:
                writer = StreamWriter(
                    self.logger, device_info, extra_info, schedule_item,
                    self.settings.default_output_config, self)
                with self.writer_lock:
                    self.writers[schedule_item.id] = writer

        with self.status_pipe_lock:
            self.status_pipe.send(
                (StreamStatus.ONGOING_ITEMS, schedule_ids_set,
                 rf_power_needed, len(self.schedule)))

    def update_writers(self, device_info: DeviceInfo, extra_info: dict,
                       schedule_items: set[ScheduleItem]) -> None:
        schedule_dict = {s.id: s for s in schedule_items}
        new_keys = set(schedule_dict.keys())
        rf_power_needed = any(s.needs_rf_power for s in schedule_items)

        with self.status_pipe_lock:
            self.status_pipe.send(
                (StreamStatus.ONGOING_ITEMS, new_keys, rf_power_needed,
                 len(self.schedule)))

        with self.writer_lock:
            running_keys = set(self.writers.keys())
            close_keys = running_keys.difference(new_keys)
            update_keys = running_keys.intersection(new_keys)
            create_keys = new_keys.difference(running_keys)
            for key in close_keys:
                # close the writer as it's no longer needed
                writer = self.writers.pop(key)
                writer.close()
                self.background_join_deque.append(writer)
            for key in update_keys:
                # update the writer with the new schedule item
                writer = self.writers[key]
                schedule_item = schedule_dict[key]
                if schedule_item.output_config:
                    try:
                        writer.update(schedule_item)
                        continue
                    except ValueError:
                        # recreate the writer
                        create_keys.add(key)

                # need to delete the writer
                del self.writers[key]
                writer.close()
                self.background_join_deque.append(writer)
            for key in create_keys:
                # create a new writer
                schedule_item = schedule_dict[key]
                if schedule_item.output_config:
                    writer = StreamWriter(
                        self.logger, device_info, extra_info, schedule_item,
                        self.settings.default_output_config, self)
                    self.writers[schedule_item.id] = writer

    def _rgb_callback(self, index: int, values: tuple[int, int, int]) -> None:
        # NOTE: called with device lock
        with self.status_pipe_lock:
            self.status_pipe.send((StreamStatus.RGB_UPDATE, index, values))

    def run_hw_tests(self) -> None:
        if not self.hw_tests:
            return

        self.logger.info("Running Hardware Tests")

        hw_test_funcs, run_id = self.hw_tests
        try:
            with self.device_lock:
                for hw_test_func, test_id in hw_test_funcs:
                    try:
                        data = hw_test_func(self.device)
                        with self.status_pipe_lock:
                            self.status_pipe.send(
                                (StreamStatus.HARDWARE_TEST_FUNCTION_FINISHED,
                                 run_id, test_id, data))
                    except Exception:
                        self.logger.exception("Failure in HW test")
        finally:
            self.hw_tests = None
            with self.status_pipe_lock:
                self.status_pipe.send(
                    (StreamStatus.HARDWARE_TEST_RUN_FINISHED, run_id))
            self.logger.info("Finished Hardware Tests")

    def run_rf_test(self) -> None:
        if self.rf_test_params is None:
            return

        self.logger.info("Starting RF Test")

        try:
            with self.device_lock:
                params = self.rf_test_params.test_params
                if isinstance(params, RFFixedTestParams):
                    self.device.do_radio_fixed_test(
                        params.channel, params.duration, params.mode)
                elif isinstance(params, RFSweepTestParams):
                    self.device.do_radio_sweep_test(
                        params.start, params.stop, params.hop_interval,
                        params.hop_count, params.mode)
                else:
                    raise ValueError("Unknown RF test type")

            while True:
                finished = self.rf_test_params.finished_pipe.poll(0.1)
                if finished:
                    # any data on the pipe means the test is done
                    break

                with self.device_lock:
                    # just do a meaningless test command
                    self.device.echo_params(b'')
        except asphodel.AsphodelError:
            pass  # this is normal behavior on WMs
        finally:
            self.rf_test_params = None

            with self.status_pipe_lock:
                self.status_pipe.send((StreamStatus.RF_TEST_FINISHED,))
            self.logger.info("Finished RF Test")

    def check_expired_schedule(self) -> bool:
        expired_items = self.schedule.get_expired_items()
        if expired_items:
            for item in expired_items:
                # NOTE: this function will delete the item from the schedule
                self.writer_stopped(item.id, False)
            return True
        else:
            return False

    def _set_device_mode_locked(self, mode: int) -> None:
        try:
            self.device.set_device_mode(mode)
            success = True
        except asphodel.AsphodelError:
            success = False
        with self.status_pipe_lock:
            self.status_pipe.send(
                (StreamStatus.DEVICE_MODE_UPDATE, success, mode))

    def _reconnect_device_locked(self, serial_number: Optional[str]) -> None:
        with self.status_pipe_lock:
            self.status_pipe.send((StreamStatus.RECONNECTING,))
        self.logger.debug("Reconnecting")
        if self.device.supports_remote_commands():
            try:
                self.device.flush()
            except asphodel.AsphodelError:
                pass  # ignore
        self.device.reconnect(serial_number=serial_number)

    def write_nvm(self, nvm: bytes, serial_number: Optional[str]) -> None:
        self.logger.debug("Start writing NVM")
        with self.device_lock:
            with self.status_pipe_lock:
                self.status_pipe.send((StreamStatus.WRITE_NVM_PROGRESS,
                                       0, len(nvm)))

            self.device.erase_nvm()

            # split up the write manually for better progress reporting
            param_len = self.device.get_max_outgoing_param_length()
            max_write_size = (param_len - 2) & ~0x03  # must be a multiple of 4
            index = 0
            while index < len(nvm):
                block = nvm[index:index + max_write_size]
                self.device.write_nvm_raw(index, block)
                index += len(block)
                with self.status_pipe_lock:
                    self.status_pipe.send((StreamStatus.WRITE_NVM_PROGRESS,
                                           index, len(nvm)))

            self.device.reset()
            self._reconnect_device_locked(serial_number)

    def _force_reset_locked(self) -> None:
        self.logger.debug("Resetting device")
        serial_number = self.device.get_serial_number()
        self.device.reset()
        self._reconnect_device_locked(serial_number=serial_number)

    def _force_run_bootloader_locked(self) -> None:
        self.logger.debug("Jumping to bootloader")
        serial_number = self.device.get_serial_number()
        self.device.bootloader_jump()
        self.device.reconnect(bootloader=True, serial_number=serial_number)

    def _force_run_app_locked(self) -> None:
        self.logger.debug("Jumping to app from bootloader")
        serial_number = self.device.get_serial_number()
        self.device.bootloader_start_program()
        self.device.reconnect(application=True, serial_number=serial_number)

    def _do_bootloader_locked(
            self, firmware_data: dict[str, Any], serial_number: str,
            device_info: DeviceInfo) -> None:
        event_data = {
            "board_type": device_info.board_info[0],
            "board_rev": device_info.board_info[1],
            "computer": platform.node(),
        }

        keys_of_interest = ["application", "bootloader", "build_date",
                            "build_info", "checksum", "source"]

        for key in keys_of_interest:
            value = firmware_data.get(key)
            if value is not None:
                event_data[key] = value

        def callback(finished: int, total: int, status_str: str) -> None:
            with self.status_pipe_lock:
                self.status_pipe.send((StreamStatus.BOOTLOADER_PROGRESS,
                                       finished, total, status_str))

        try:
            do_bootload(self.device, serial_number, self.logger, firmware_data,
                        callback)
            sucess = True
        except Exception:
            self.logger.exception("Firmware update failed")
            sucess = False

        with self.status_pipe_lock:
            self.status_pipe.send((StreamStatus.BOOTLOADER_FINISHED,
                                   sucess, event_data))

    def get_device_info_callback(self, finished: int, total: int,
                                 section_name: str) -> None:
        with self.status_pipe_lock:
            self.status_pipe.send((StreamStatus.DEVICE_INFO_PROGRESS, finished,
                                   total, section_name))

    def get_device_info(self, allow_reconnect: bool) -> DeviceInfo:
        with self.device_lock:
            device_info = get_device_info(
                self.device, allow_reconnect, self.device_info_logger,
                self.diskcache, self.get_device_info_callback)
        return device_info

    @staticmethod
    def get_active_streams(
            device_info: DeviceInfo,
            schedule_items: set[ScheduleItem]) -> frozenset[int]:
        desired: set[int] = set()
        for item in schedule_items:
            if item.active_streams is None:
                # wants all streams
                return frozenset(range(len(device_info.streams)))
            else:
                desired.update(item.active_streams)

        return frozenset(desired)

    def calc_stream_counts(
            self, device_info: DeviceInfo,
            active_streams: frozenset[int]) -> tuple[int, int, int]:
        if len(active_streams) == 0:
            # use a fallback value for stream_counts
            stream_counts = (1, 1, self.settings.timeout)
        else:
            streams = [device_info.streams[i] for i in sorted(active_streams)]

            stream_counts = asphodel.nativelib.get_streaming_counts(
                streams,
                response_time=self.settings.response_time / 1000,
                buffer_time=self.settings.buffer_time / 1000,
                timeout=self.settings.timeout)
        return stream_counts

    def update_settings(self, new_settings: StreamSettings) -> bool:
        if new_settings == self.settings:
            return False

        if (new_settings.response_time != self.settings.response_time or
                new_settings.buffer_time != self.settings.buffer_time or
                new_settings.timeout != self.settings.timeout or
                new_settings.default_output_config !=
                self.settings.default_output_config):
            # can't change these on the fly, restart streaming
            self.settings = new_settings
            return True

        with self.device_lock:
            self.rgb_manager.set_auto_rgb_locked(new_settings.auto_rgb)

        self.settings = new_settings

        return False

    def process_message(self, device_info: DeviceInfo,
                        message: tuple[Any, ...]) -> Union[bool, bytes]:
        message_type = message[0]

        if message_type == StreamControl.CHANGE_SETTINGS:
            new_settings: StreamSettings = message[1]
            return self.update_settings(new_settings)
        elif message_type == StreamControl.UPDATE_SCHEDULE_ITEM:
            item: ScheduleItem = message[1]
            self.schedule.update_item(item)
            if self.parent_controller:
                self.parent_controller.schedule_changed()
            if self.subcontroller:
                self.subcontroller.schedule_changed()
        elif message_type == StreamControl.DELETE_SCHEDULE_IDS:
            item_ids: list[str] = message[1]
            for item_id in item_ids:
                self.schedule.delete_item_id(item_id)
            if self.parent_controller:
                self.parent_controller.schedule_changed()
            if self.subcontroller:
                self.subcontroller.schedule_changed()
        elif message_type == StreamControl.SET_RGB:
            index = message[1]
            values = message[2]
            with self.device_lock:
                self.rgb_manager.set_rgb_locked(index, values)
        elif message_type == StreamControl.GET_RGB_STATE:
            with self.status_pipe_lock:
                for index, values in enumerate(device_info.rgb_settings):
                    self.status_pipe.send((StreamStatus.RGB_UPDATE, index,
                                           values))
        elif message_type == StreamControl.SET_LED:
            index = message[1]
            value = message[2]
            with self.device_lock:
                self.device.set_led_value(index, value)
        elif message_type == StreamControl.SET_CTRL_VAR:
            index = message[1]
            value = message[2]
            with self.device_lock:
                self.device.set_ctrl_var(index, value)
        elif message_type == StreamControl.SET_DEVICE_MODE:
            mode = message[1]
            with self.device_lock:
                self._set_device_mode_locked(mode)
        elif message_type == StreamControl.SET_RF_POWER:
            enable = message[1]
            with self.device_lock:
                self.device.enable_rf_power(enable)
        elif message_type == StreamControl.WRITE_NVM:
            desired_nvm: bytes = message[1]
            return desired_nvm
        elif message_type == StreamControl.FORCE_RESET:
            # schedule reset for beginning of next loop
            self.reset_function = self._force_reset_locked
            return True
        elif message_type == StreamControl.FORCE_RUN_BOOTLOADER:
            # schedule reset for beginning of next loop
            self.reset_function = self._force_run_bootloader_locked
            return True
        elif message_type == StreamControl.FORCE_RUN_APPLICATION:
            # schedule reset for beginning of next loop
            self.reset_function = self._force_run_app_locked
            return True
        elif message_type == StreamControl.DO_BOOTLOADER:
            firmware_data = message[1]
            self.reset_function = functools.partial(
                self._do_bootloader_locked, firmware_data,
                device_info.serial_number, device_info)
            return True
        elif message_type == StreamControl.DO_HARDWARE_TESTS:
            funcs = message[1]
            run_id = message[2]
            self.hw_tests = (funcs, run_id)
            return True
        elif message_type == StreamControl.DO_RF_TEST:
            params = message[1]
            self.rf_test_params = params
            return True
        elif message_type == StreamControl.DO_ACTIVE_SCAN:
            self.radio_queue.put(message)
        elif message_type == StreamControl.DO_RADIO_FUNCTION:
            self.radio_queue.put(message)
        elif message_type == StreamControl.ACTIVE_TRIGGERS_CHANGED:
            active_triggers: frozenset[str] = message[1]
            self.schedule.set_active_triggers(active_triggers)

        # don't stop process loop
        return False

    def process_loop(
            self, device_info: DeviceInfo, extra_info: dict,
            ready_items: set[ScheduleItem], nvm: bytes,
            active_streams: frozenset[int],
            remote_info: Optional[tuple[int, bool]]) -> Optional[bytes]:
        while not self.finished.is_set():  # process loop
            if self.disconnected.is_set():
                return None

            # process all connection items
            while True:
                try:
                    message = self.ctrl_queue.get_nowait()
                    result = self.process_message(device_info, message)
                    if result is False:
                        # keep
                        continue
                    elif result is True:
                        return None
                    else:
                        return result  # bytes
                except Empty:
                    break

            # see if ready_items has changed
            new_ready, next_change = self.schedule.get_ready_items()

            if new_ready == ready_items:
                if self.check_expired_schedule():
                    # some expired items were removed, check again
                    new_ready, next_change = self.schedule.get_ready_items()

            if new_ready != ready_items:
                # something has changed, look more closely
                new_schedule, new_nvm, new_remote = get_compatible_set(
                    new_ready, device_info, nvm)

                # see if nvm changed
                if new_nvm != nvm:
                    # NOTE: don't return new NVM here because the outer loop
                    # will figure it out fresh when it calculates the schedule
                    return None

                # see if active streams have changed
                new_active_streams = self.get_active_streams(
                    device_info, new_schedule)
                if new_active_streams != active_streams:
                    return None

                if new_remote != remote_info:
                    remote_info = new_remote

                    if remote_info is not None:
                        passed_remote_info = RemoteInfo(*remote_info)
                    else:
                        passed_remote_info = None

                    self.radio_queue.put(
                        (StreamControl._REMOTE_INFO, passed_remote_info))

                # nothing device side has changed, only the schedule. Do the
                # necessary updates to the writers
                ready_items = new_ready
                self.update_writers(device_info, extra_info, new_schedule)

            # get the maximum amount of time to wait
            if next_change is not None:
                wait_time = min(10.0, next_change)
            else:
                wait_time = 10.0

            try:
                message = self.ctrl_queue.get(block=True, timeout=wait_time)

                # just woke up after a long sleep, check events
                if self.finished.is_set():
                    return None
                if self.disconnected.is_set():
                    return None

                # process the message
                result = self.process_message(device_info, message)
                if result is False:
                    # keep
                    continue
                elif result is True:
                    return None
                else:
                    return result  # bytes
            except Empty:
                pass

        return None

    def stream_thread_run(self) -> None:
        connected: bool = True  # class is initialized with connected device
        allow_reconnect: bool = False
        device_info: Optional[DeviceInfo] = None
        serial_number: Optional[str] = None
        desired_nvm: Optional[bytes] = None

        try:
            while not self.finished.is_set():
                if not connected:
                    device_info = None
                    try:
                        with self.device_lock:
                            self._reconnect_device_locked(serial_number)
                    except asphodel.AsphodelError:
                        self.logger.exception("Could not reconnect to device")
                        with self.status_pipe_lock:
                            self.status_pipe.send((StreamStatus.DISCONNECTED,))
                        # all done
                        return
                    connected = True

                try:
                    if self.reset_function:
                        try:
                            with self.device_lock:
                                self.reset_function()
                        finally:
                            self.reset_function = None
                            device_info = None
                            allow_reconnect = False
                        continue

                    if self.hw_tests:
                        try:
                            self.run_hw_tests()
                        finally:
                            device_info = None
                            allow_reconnect = False
                        continue

                    if self.rf_test_params:
                        try:
                            self.run_rf_test()
                        finally:
                            device_info = None
                            allow_reconnect = False
                        continue

                    with self.status_pipe_lock:
                        self.status_pipe.send(
                            (StreamStatus.DEVICE_INFO_START,))

                    if device_info is None:
                        device_info = self.get_device_info(allow_reconnect)
                        serial_number = device_info.serial_number

                    with self.device_lock:
                        self.rgb_manager.connected_locked(device_info)

                    ready_items, _next_change = self.schedule.get_ready_items()

                    if desired_nvm is None:
                        desired_nvm = device_info.nvm

                    # TODO: check ready_items's nvm compatability and finish
                    # any items with an error that raise an exception when
                    # trying to create a valid nvm configuration.
                    # This would be pretty easy to test using a device switched
                    # into the bootloader, where there aren't any settings

                    schedule_items, nvm, remote_info = get_compatible_set(
                        ready_items, device_info, desired_nvm)

                    # write the new NVM, if necessary
                    desired_nvm = None
                    if nvm != device_info.nvm:
                        allow_reconnect = False
                        device_info = None

                        # write the new NVM, reset and reconnect
                        self.write_nvm(nvm, serial_number)

                        # restart the connect loop to get fresh device info
                        continue
                    elif device_info.nvm_modified:
                        allow_reconnect = False
                        device_info = None

                        # reset the device
                        with self.device_lock:
                            self.device.reset()
                            self._reconnect_device_locked(
                                serial_number=serial_number)

                        # restart the connect loop to get fresh device info
                        continue

                    with self.status_pipe_lock:
                        self.status_pipe.send(
                            (StreamStatus.DEVICE_INFO_READY, device_info))

                    # determine the active streams
                    active_streams = self.get_active_streams(
                        device_info, schedule_items)

                    extra_info: dict[str, Any] = {
                        'streams_to_activate': sorted(active_streams),
                    }

                    if active_streams:
                        stream_counts = self.calc_stream_counts(
                            device_info, active_streams)
                        extra_info['stream_counts'] = stream_counts
                    else:
                        stream_counts = None

                    self.start_writers(device_info, extra_info, schedule_items)

                    # send device info and active streams through packet pipe
                    # NOTE: packet thread is not running, so this is safe
                    if self.packet_pipe is not None:
                        self.packet_pipe.send((device_info, active_streams))

                    try:
                        with self.device_lock:
                            self.flush_packets()
                            if stream_counts:
                                self.device.start_streaming_packets(
                                    *stream_counts,
                                    callback=self.packet_callback)
                            self.device.set_connect_callback(
                                self.connect_callback)
                            if stream_counts:
                                self.start_streams(device_info, active_streams)
                            self.rgb_manager.streaming_locked()

                        with self.status_pipe_lock:
                            self.status_pipe.send(
                                (StreamStatus.STREAMING_STARTED,
                                 active_streams))

                        allow_reconnect = True

                        self.disconnected.clear()

                        # start background threads
                        if active_streams:
                            self.packet_thread = threading.Thread(
                                target=self.packet_thread_run)
                            self.packet_thread.start()
                        else:
                            self.check_connection_thread = threading.Thread(
                                target=self.check_connection_thread_run)
                            self.check_connection_thread.start()

                        if device_info.supports_rf_power:
                            self.rf_power_thread = threading.Thread(
                                target=self.rf_power_thread_run)
                            self.rf_power_thread.start()

                        if device_info.supports_radio:
                            if remote_info is not None:
                                passed_remote_info = RemoteInfo(*remote_info)
                            else:
                                passed_remote_info = None

                            self.radio_thread = threading.Thread(
                                target=self.radio_thread_run,
                                args=(device_info, passed_remote_info))
                            self.radio_thread.start()

                        # handle schedule changes and incoming control messages
                        self.logger.debug("Entering process loop")
                        desired_nvm = self.process_loop(
                            device_info, extra_info, ready_items, nvm,
                            active_streams, remote_info)
                        self.logger.debug("Exiting process loop")

                        if self.disconnected.is_set():
                            # exited the process loop abnormally
                            self.logger.debug("exited process loop abnormally")
                            connected = False
                    finally:
                        self.logger.debug("Stopping streaming")
                        with self.device_lock:
                            try:
                                # NOTE: these two can't fail in practice
                                self.device.set_connect_callback(None)
                                self.device.stop_streaming_packets()

                                self.device.poll_device(0)
                                self.stop_streams(active_streams)
                                self.rgb_manager.disconnected_locked()
                            except asphodel.AsphodelError:
                                pass  # probably disconnected, ignore
                except asphodel.AsphodelError:
                    self.logger.exception("Device Error")
                    # start from scratch
                    connected = False
                    device_info = None
                    desired_nvm = None
                    continue
                finally:
                    self.stop_all_writers()

                    with self.status_pipe_lock:
                        try:
                            self.status_pipe.send(
                                (StreamStatus.ONGOING_ITEMS, set(), False,
                                 len(self.schedule)))
                        except Exception:
                            pass  # pipe already closed: ignore

                    # stop and join background threads
                    self.disconnected.set()
                    if self.packet_thread:
                        self.packet_thread.join()
                        self.packet_thread = None
                    if self.check_connection_thread:
                        self.check_connection_thread.join()
                        self.check_connection_thread = None
                    if self.radio_thread:
                        self.radio_thread.join()
                        self.radio_thread = None
                        self._empty_radio_queue()
                    if self.rf_power_thread:
                        self.rf_power_thread.join()
                        self.rf_power_thread = None

                    # NOTE: packet thread is not running, so this is safe
                    if self.packet_pipe is not None:
                        self.packet_pipe.send(None)
        except Exception:
            self.logger.exception("Unhandled exception in stream_thread_run")
            with self.status_pipe_lock:
                try:
                    self.status_pipe.send(
                        (StreamStatus.STREAMING_ERROR_OTHER, 0))
                except Exception:
                    pass  # pipe already closed: ignore
            self.stop_all_writers()
            with self.status_pipe_lock:
                try:
                    self.status_pipe.send(
                        (StreamStatus.ONGOING_ITEMS, set(), False,
                         len(self.schedule)))
                except Exception:
                    pass  # pipe already closed: ignore

    def flush_packets(self) -> None:  # call with device lock
        stream_size = self.device.get_stream_packet_length()
        start_time = time.monotonic()
        while time.monotonic() - start_time < 0.5:
            try:
                self.device.get_stream_packets_blocking(stream_size * 10, 50)
            except asphodel.AsphodelError as e:
                if e.errno == -7:  # ASPHODEL_TIMEOUT
                    break
                else:
                    raise

    def start_streams(
            self, device_info: DeviceInfo,
            active_streams: frozenset[int]) -> None:  # call with device lock
        stream_ids = sorted(active_streams)

        # warm up streams
        for stream_id in stream_ids:
            self.device.warm_up_stream(stream_id, True)

        warm_up_time = 0.0
        for stream_id in stream_ids:
            stream = device_info.streams[stream_id]
            if stream.warm_up_delay > warm_up_time:
                warm_up_time = stream.warm_up_delay

        if warm_up_time > 0.0:
            time.sleep(warm_up_time)

        # enable streams
        for stream_id in stream_ids:
            self.device.enable_stream(stream_id, True)

            # disable warm up so we don't have to worry about it later
            self.device.warm_up_stream(stream_id, False)

    def stop_streams(
            self,
            active_streams: frozenset[int]) -> None:  # call with device lock
        for stream_id in sorted(active_streams):
            self.device.enable_stream(stream_id, False)

    def packet_callback(self, status: int,
                        stream_packets: list[bytes]) -> None:
        if status == -7:  # ASPHODEL_TIMEOUT
            if not self.disconnected.is_set():
                self.disconnected.set()
                self.ctrl_queue.put((StreamControl._WAKEUP,))
                with self.status_pipe_lock:
                    self.status_pipe.send(
                        (StreamStatus.STREAMING_ERROR_TIMEOUT,))
        elif status != 0:
            if not self.disconnected.is_set():
                self.disconnected.set()
                self.ctrl_queue.put((StreamControl._WAKEUP,))
                with self.status_pipe_lock:
                    self.status_pipe.send(
                        (StreamStatus.STREAMING_ERROR_OTHER, status))
        else:
            if self.packet_pipe is not None:
                self.packet_pipe.send(stream_packets)
            with self.writer_lock:
                for writer in self.writers.values():
                    writer.write(stream_packets)

    def connect_callback(self, _status: int, connected: int) -> None:
        try:
            if not connected:
                self.disconnected.set()
                self.ctrl_queue.put((StreamControl._WAKEUP,))

                # remove callback
                try:
                    self.device.set_connect_callback(None)
                except asphodel.AsphodelError:
                    pass  # probably the remote wrapper has been closed

                with self.status_pipe_lock:
                    self.status_pipe.send(
                        (StreamStatus.STREAMING_ERROR_DISCONNECT,))
        except Exception:
            self.logger.exception("Unhandled exception in connect_callback")

    def packet_thread_run(self) -> None:
        try:
            while not self.disconnected.is_set():
                self.device.poll_device(100)
        except Exception:
            self.logger.exception("Uncaught exception in packet_thread_run")
            self.disconnected.set()
            self.ctrl_queue.put((StreamControl._WAKEUP,))
            with self.status_pipe_lock:
                self.status_pipe.send(
                    (StreamStatus.STREAMING_ERROR_DISCONNECT,))

    def check_connection_thread_run(self) -> None:
        while True:
            if self.disconnected.wait(timeout=0.1):
                break

            if self.device_lock.acquire(blocking=False):
                try:
                    # just do a meaningless test command
                    self.device.echo_params(b'')
                except asphodel.AsphodelError:
                    self.disconnected.set()
                    self.ctrl_queue.put((StreamControl._WAKEUP,))
                    with self.status_pipe_lock:
                        self.status_pipe.send(
                            (StreamStatus.STREAMING_ERROR_DISCONNECT,))
                finally:
                    self.device_lock.release()

    def rf_power_thread_run(self) -> None:
        try:
            while True:
                if self.disconnected.wait(1):
                    return

                with self.device_lock:
                    self.device.reset_rf_power_timeout(5000)
        except Exception:
            self.logger.exception("Uncaught exception in rf_power_thread_run")
        finally:
            with self.device_lock:
                try:
                    self.logger.debug("Relinquishing control of RF Power")
                    self.device.reset_rf_power_timeout(1)
                except asphodel.AsphodelError:
                    # device is probably disconnected
                    pass

    def _do_active_scan_locked(self, serial: int, bootloader: bool) -> None:
        try:
            if not bootloader:
                self.logger.debug("Starting active scan on %s", serial)
                self.device.connect_radio(serial)
            else:
                self.logger.debug(
                    "Starting bootloader active scan on %s", serial)
                self.device.connect_radio_boot(serial)

            self.remote.wait_for_connect(1000)

            active_scan = get_active_scan_info(
                self.remote, self.device_info_logger, self.diskcache)
            self.logger.debug("Finished active scan on %s", serial)
        except Exception:
            # couldn't do the active scan
            # no big deal
            active_scan = None
            self.logger.debug("Failed active scan on %s", serial)
        finally:
            self.device.stop_radio()
        with self.status_pipe_lock:
            self.status_pipe.send(
                (StreamStatus.ACTIVE_SCAN_DATA, serial, active_scan))

    def _collect_scan_results_locked(self, device_info: DeviceInfo) -> bool:
        last_seen = datetime.datetime.now(datetime.timezone.utc)

        # get the results
        results = self.device.get_radio_extra_scan_results()

        # get the scan powers
        scan_powers: dict[int, int] = {}  # key: sn, value: power dBm
        if device_info.radio_scan_power is True:
            power_max_queries = min(
                device_info.max_outgoing_param_length // 4,
                device_info.max_incoming_param_length)

            for i in range(0, len(results), power_max_queries):
                result_subset = results[i:i + power_max_queries]
                serials = [r.serial_number for r in result_subset]
                powers = self.device.get_radio_scan_power(serials)
                for sn, power in zip(serials, powers):
                    if power != 0x7F:
                        scan_powers[sn] = power

        scans: list[ScanResult] = []

        for r in results:
            power = scan_powers.get(r.serial_number, None)  # type: ignore
            board_info = get_remote_board_info(r.serial_number, self.diskcache)
            scans.append(ScanResult(
                serial_number=r.serial_number,
                last_seen=last_seen,
                bootloader=bool(r.asphodel_type &
                                asphodel.ASPHODEL_PROTOCOL_TYPE_BOOTLOADER),
                asphodel_type=r.asphodel_type,
                device_mode=r.device_mode,
                scan_strength=power,
                board_info=board_info))

        if scans:
            with self.status_pipe_lock:
                self.status_pipe.send(
                    (StreamStatus.SCAN_DATA, scans))

        return not scans  # empty

    def _do_scan(self, device_info: DeviceInfo) -> None:
        try:
            with self.device_lock:
                self.device.start_radio_scan()

            end_time = time.monotonic() + 0.6  # 600 ms
            while time.monotonic() < end_time:
                with self.device_lock:
                    empty = self._collect_scan_results_locked(device_info)

                if self.disconnected.is_set() or not self.radio_queue.empty():
                    return

                if empty:
                    time.sleep(0.001)  # use less CPU
        finally:
            with self.device_lock:
                self.device.stop_radio()

    def _do_bootloader_scan(self, device_info: DeviceInfo) -> None:
        try:
            with self.device_lock:
                self.device.start_radio_scan_boot()

            end_time = time.monotonic() + 0.1  # 100 ms

            while time.monotonic() < end_time:
                with self.device_lock:
                    empty = self._collect_scan_results_locked(device_info)

                if self.disconnected.is_set() or not self.radio_queue.empty():
                    return

                if empty:
                    time.sleep(0.001)  # use less CPU
        finally:
            with self.device_lock:
                self.device.stop_radio()

    def _start_connect_locked(self, remote_info: RemoteInfo) -> None:
        if not remote_info.bootloader:
            self.logger.info(
                "Starting connect to %s", remote_info.serial_number)
            self.device.connect_radio(remote_info.serial_number)
        else:
            self.logger.info("Starting bootloader connect to %s",
                             remote_info.serial_number)
            self.device.connect_radio_boot(remote_info.serial_number)
        with self.status_pipe_lock:
            self.status_pipe.send(
                (StreamStatus.REMOTE_CONNECTING, remote_info.serial_number,
                 remote_info.bootloader))

    def _stop_subcontroller_locked(self, serial_number: Optional[int]) -> None:
        if self.subcontroller:
            if serial_number is None:
                self.logger.debug("Stopping subcontroller")
            else:
                self.logger.debug("Stopping subcontroller for %s",
                                  serial_number)
            self.subcontroller.stop()
            self.subcontroller = None
            self.rgb_manager.remote_disconnected_locked()
        if self.remote_wrapper:
            if self.remote_wrapper.remote:
                self.remote_wrapper.remote.set_connect_callback(None)
                self.remote_wrapper.remote = None
            self.remote_wrapper = None

    def _start_disconnect_locked(self, serial_number: int) -> None:
        self.logger.info("Starting disconnect from %s", serial_number)
        self._stop_subcontroller_locked(serial_number)
        self.device.stop_radio()
        with self.status_pipe_lock:
            self.status_pipe.send(
                (StreamStatus.REMOTE_DISCONNECTED,))

    def _empty_radio_queue(self) -> None:
        while True:
            try:
                message = self.radio_queue.get(False)
                message_type = message[0]

                if message_type == StreamControl.DO_ACTIVE_SCAN:
                    serial_number = message[1]
                    with self.status_pipe_lock:
                        self.status_pipe.send((StreamStatus.ACTIVE_SCAN_DATA,
                                               serial_number, None))
                elif message_type == StreamControl.DO_RADIO_FUNCTION:
                    with self.status_pipe_lock:
                        self.status_pipe.send(
                            (StreamStatus.RADIO_FUNCTION_FINISHED, False,
                             None))
                elif message_type == StreamControl._REMOTE_INFO:
                    pass  # ignore
                elif message_type == StreamControl._REMOTE_CLOSED:
                    pass  # ignore
                else:
                    self.logger.warning("Unknown radio message %s", message)
            except Empty:
                break

    def radio_thread_run(self, device_info: DeviceInfo,
                         remote_info: Optional[RemoteInfo]) -> None:
        try:
            connected = False
            first_pass = True
            last_remote_info: Optional[RemoteInfo] = None

            with self.device_lock:
                self.device.stop_radio()
                self.remote = self.device.get_remote_device()
                self.remote.open()

            while not self.disconnected.is_set():
                # check queue
                while True:
                    try:
                        message = self.radio_queue.get(False)
                        message_type = message[0]

                        if message_type == StreamControl.DO_ACTIVE_SCAN:
                            serial_number = message[1]
                            bootloader = message[2]
                            if remote_info:
                                # this got submitted after the connect request
                                self.logger.debug("Ignoring active scan on %s",
                                                  serial_number)
                                with self.status_pipe_lock:
                                    self.status_pipe.send(
                                        (StreamStatus.ACTIVE_SCAN_DATA,
                                         serial_number, None))
                                continue
                            with self.device_lock:
                                self._do_active_scan_locked(serial_number,
                                                            bootloader)
                        elif message_type == StreamControl.DO_RADIO_FUNCTION:
                            func = message[1]
                            with self.device_lock:
                                result = func(self.device, self.remote,
                                              self.logger)
                                with self.status_pipe_lock:
                                    self.status_pipe.send(
                                        (StreamStatus.RADIO_FUNCTION_FINISHED,
                                         True, result))
                        elif message_type == StreamControl._REMOTE_INFO:
                            remote_info = message[1]
                            break  # handle this one before the next
                        elif message_type == StreamControl._REMOTE_CLOSED:
                            if last_remote_info is not None:
                                # disconnect the old
                                with self.device_lock:
                                    self._start_disconnect_locked(
                                        last_remote_info.serial_number)
                            connected = False
                            last_remote_info = None
                        else:
                            self.logger.warning(
                                "Unknown radio message %s", message)
                    except Empty:
                        break

                if last_remote_info != remote_info:
                    connected = False

                    if last_remote_info is not None:
                        # disconnect the old
                        with self.device_lock:
                            self._start_disconnect_locked(
                                last_remote_info.serial_number)

                    if remote_info is None:
                        first_pass = True
                    else:
                        # connect
                        with self.device_lock:
                            self._start_connect_locked(remote_info)

                    last_remote_info = remote_info

                if remote_info:
                    if not connected:
                        with self.device_lock:
                            status = self.device.get_radio_status()
                            if status[0]:
                                sn_str = self.remote.get_serial_number()
                                if sn_str:
                                    connected = True
                                    with self.status_pipe_lock:
                                        self.current_remote_info = remote_info
                                        self.status_pipe.send(
                                            (StreamStatus.REMOTE_CONNECTED,
                                             status[1], sn_str,
                                             remote_info.bootloader))
                                else:
                                    # immediate disconnect, start again
                                    self._start_connect_locked(remote_info)
                            elif status[1] == 0:
                                # immediate disconnect, start again
                                self._start_connect_locked(remote_info)
                    else:
                        self.disconnected.wait(0.1)
                else:
                    # do radio scan
                    self._do_scan(device_info)
                    if self.disconnected.is_set():
                        break
                    if not self.radio_queue.empty():
                        continue

                    # do bootloader scan
                    self._do_bootloader_scan(device_info)
                    if self.disconnected.is_set():
                        break
                    if not self.radio_queue.empty():
                        continue

                    # send first pass message if necessary
                    if first_pass:
                        first_pass = False
                        with self.status_pipe_lock:
                            self.status_pipe.send(
                                (StreamStatus.SCAN_FIRST_PASS,))
        except Exception:
            self.logger.exception("Uncaught exception in radio_thread_run")
        finally:
            with self.device_lock:
                self.logger.debug("Stopping radio thread")

                self._stop_subcontroller_locked(None)

                try:
                    self.device.stop_radio()
                except asphodel.AsphodelError:
                    # device is probably disconnected
                    pass

                try:
                    self.remote.close()
                except asphodel.AsphodelError:
                    # device is probably disconnected
                    pass

    def get_remote_schedule(self, schedule_items: Iterable[ScheduleItem],
                            remote_info: RemoteInfo) -> RemoteSchedule:
        schedule: Schedule = self.schedule  # type: ignore
        return RemoteSchedule(schedule, remote_info.serial_number,
                              remote_info.bootloader, schedule_items)

    def register_subcontroller_locked(
            self, subcontroller: "StreamController") -> None:
        self.subcontroller = subcontroller
        self.rgb_manager.remote_connected_locked()

    def unregister_subcontroller_locked(
            self, subcontroller: "StreamController") -> None:
        if self.subcontroller == subcontroller:
            self.subcontroller = None
            self.radio_queue.put((StreamControl._REMOTE_CLOSED,))
            try:
                self.rgb_manager.remote_disconnected_locked()
            except Exception:
                pass  # ignore, probably disconnection in progress

    def clean_up_remote(self, remote_wrapper: RemoteWrapper) -> None:
        # NOTE: this is called with device_lock directly by proxy_remote

        if self.remote_wrapper == remote_wrapper:
            self.remote_wrapper = None

        if remote_wrapper.remote:
            remote_wrapper.remote.set_connect_callback(None)
            remote_wrapper.remote = None

    def get_remote(self, serial_number: int,
                   bootloader: bool) -> RemoteWrapper:
        # NOTE: this is called with device_lock directly by proxy_remote

        remote_info = RemoteInfo(serial_number, bootloader)
        wrapper = RemoteWrapper(self.remote, self, remote_info)

        # clean up any left overs
        self.remote.set_connect_callback(None)
        self.remote.stop_streaming_packets()
        self.remote.poll_device(0)

        # set up a clean up function
        proxy_remote.register_device_cleanup(
            cast(asphodel.AsphodelNativeDevice, wrapper), self.clean_up_remote)

        self.remote_wrapper = wrapper
        return wrapper
