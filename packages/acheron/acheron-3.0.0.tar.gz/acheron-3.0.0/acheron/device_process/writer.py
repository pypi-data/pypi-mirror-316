import binascii
import ctypes
from dataclasses import fields
import datetime
import json
import logging
import os
from queue import Empty, Queue
import re
import struct
import subprocess
import sys
import threading
import time
from typing import Any, IO, Iterable, Optional, Protocol
import unicodedata

from asphodel.device_info import DeviceInfo

from .compressor import open_compressor
from .schedule import OutputConfig, ScheduleItem

logger = logging.getLogger(__name__)


UPLOAD_EXTENSION = ".upload"


class WriterStatusCallback(Protocol):
    def writer_file_started(self, filename: str, schedule_id: str,
                            marked_for_upload: bool) -> None:
        ...

    def writer_file_finished(self, filename: str, schedule_id: str,
                             marked_for_upload: bool) -> None:
        ...

    def writer_stopped(self, schedule_id: str, success: bool) -> None:
        ...


def _get_valid_filename(s: str) -> str:
    # remove any non-ascii characters, and convert accents to closest ascii
    b = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    s = b.decode("ascii")

    # make any spaces into underscores
    s = s.strip().replace(" ", "_")

    # remove anything that's not alphanumeric, dash, underscore, dot
    s = re.sub(r'[^-\w.]', "", s)

    # reduce any strings of dots to a single dot
    s = re.sub(r'[.]{2,}', ".", s)

    # remove any leading or trailing dots
    s = s.strip(".")

    return s


class StreamWriter:

    def __init__(self, logger: logging.LoggerAdapter, device_info: DeviceInfo,
                 extra_info: dict, schedule_item: ScheduleItem,
                 default_output_config: OutputConfig,
                 writer_status_callback: WriterStatusCallback):
        self.logger = logger
        self.device_info = device_info
        self.extra_info = extra_info
        self.schedule_item = schedule_item
        self.default_output_config = default_output_config
        self.writer_status_callback = writer_status_callback

        if schedule_item.output_config is None:
            raise ValueError("No output configuration")
        elif schedule_item.output_config is True:
            self.output_config = default_output_config
        else:
            self.output_config = schedule_item.output_config

        self.next_boundary: Optional[datetime.datetime] = None
        self.collection_time_target: Optional[datetime.datetime] = \
            self.schedule_item.collection_time
        self.collection_time_actual: Optional[datetime.datetime] = None
        self.stop_time_target: Optional[datetime.datetime] = None
        self.stop_time_reached: bool = False
        self.current_filename: Optional[str] = None
        self.compressor_pipe: Optional[IO[bytes]] = None
        self.compressor_lock = threading.Lock()
        self.compressors: dict[str, subprocess.Popen] = {}
        self.finished_queue: Queue[str] = Queue()
        self.monitor_thread = threading.Thread(target=self.monitor_loop)

        self.packet_leader_struct = struct.Struct(">dI")

        self.is_finished = threading.Event()
        self.write_loop_exited = threading.Event()
        self.write_queue: Queue[tuple[bytes, datetime.datetime]] = Queue()
        self.write_thread = threading.Thread(target=self.write_loop)

        self.calc_filename_parts()

        self.create_header()
        self.write_thread.start()
        self.monitor_thread.start()

    def calc_filename_parts(self) -> None:
        if self.device_info.user_tag_1 is None:
            self.display_name = self.device_info.serial_number
        else:
            self.display_name = _get_valid_filename(
                self.device_info.user_tag_1)
            if not self.display_name:
                self.display_name = self.device_info.serial_number

        base_name = self.output_config.base_name
        if base_name:
            self.base_name = base_name
        else:
            self.base_name = self.display_name

        device_directory = self.output_config.device_directory
        if device_directory is False:
            self.device_directory = ""
        elif device_directory is True:
            self.device_directory = self.display_name
        else:
            self.device_directory = device_directory

    def create_header(self) -> None:
        timestamp = datetime.datetime.now(datetime.timezone.utc).timestamp()

        header_dict = {}
        for field in fields(self.device_info):
            item = getattr(self.device_info, field.name)
            header_dict[field.name] = item
        header_dict.update(self.extra_info)
        header_dict['schedule_id'] = self.schedule_item.id

        def type_convert(t: Any) -> Any:
            if t is None:
                return t
            elif isinstance(t, (int, bool, str, float)):
                return t
            elif isinstance(t, bytes):
                return binascii.b2a_hex(t).decode('ascii')
            elif isinstance(t, (list, tuple)):
                return [type_convert(x) for x in t]
            elif isinstance(t, dict):
                return {k: type_convert(v) for k, v in t.items()}
            else:
                try:
                    return t.to_json_obj()
                except AttributeError:
                    return repr(t)

        d = type_convert(header_dict)
        hb = json.dumps(d, ensure_ascii=True).encode('ascii')

        self.header_bytes = (struct.pack(">dI", timestamp, len(hb)) + hb)

    def get_filename(self, dt: datetime.datetime) -> str:
        # figure out the directory
        if self.output_config.date_dir_structure:
            date_dir = dt.strftime("%Y_%m_%d")
        else:
            date_dir = ""
        directory = os.path.join(
            self.output_config.base_directory, date_dir, self.device_directory)

        # make sure the directory exists (recursively)
        os.makedirs(directory, exist_ok=True)

        # generate the base part of the filename (no extension)
        if self.output_config.datetime_filename:
            base_name = dt.strftime("%Y%m%dT%H%MZ_") + self.base_name
        else:
            base_name = self.base_name
        base_name = os.path.join(directory, base_name)

        # create a unique filename, accounting for existing files
        filename = base_name + ".apd"
        index = 1
        while os.path.exists(filename):
            filename = base_name + "(" + str(index) + ").apd"
            index += 1

        return filename

    def open_compressor(self, dt: datetime.datetime) -> None:
        filename = self.get_filename(dt)
        self.current_filename = filename

        pipe, process = open_compressor(
            filename, self.output_config.compression_level)
        self.compressor_pipe = pipe
        if process:
            with self.compressor_lock:
                self.compressors[filename] = process

        pipe.write(self.header_bytes)

        if self.output_config.upload_marker:
            # create a .upload file to mark it for uploading
            path, name = os.path.split(filename)
            uploadfilename = os.path.join(path, "." + name + UPLOAD_EXTENSION)
            with open(uploadfilename, 'w', encoding="ascii") as uploadfile:
                # Put some contents into the file. Doesn't even matter what.
                # The background scan won't touch anything with contents until
                # it's at least 20 minutes old (when the writing process is
                # presumed to have crashed).
                uploadfile.write('in progress')
            if sys.platform == "win32":
                # make the file hidden on windows
                # the leading . in the filename is enough for linux
                ctypes.windll.kernel32.SetFileAttributesW(uploadfilename, 0x02)

        try:
            self.writer_status_callback.writer_file_started(
                filename, self.schedule_item.id,
                self.output_config.upload_marker)
        except Exception:
            self.logger.exception("Exception in writer_file_started callback")

    def close_compressor(self) -> None:
        if self.compressor_pipe:
            self.compressor_pipe.close()
            self.compressor_pipe = None

    def mark_finished(self, filename: Optional[str]) -> None:
        if filename:
            self.finished_queue.put(filename)

    def write(self, stream_packets: Iterable[bytes]) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        self.write_queue.put((b"".join(stream_packets), now))

    def calc_stop_time_target(self) -> None:
        t: Optional[datetime.datetime] = None
        if self.collection_time_actual and self.schedule_item.duration:
            t = self.collection_time_actual + self.schedule_item.duration

        if self.schedule_item.stop_time:
            if t:
                t = min(t, self.schedule_item.stop_time)
            else:
                t = self.schedule_item.stop_time

        if self.schedule_item.failure_time:
            if t:
                t = min(t, self.schedule_item.failure_time)
            else:
                t = self.schedule_item.stop_time

        self.stop_time_target = t

    def calc_next_boundary(self, dt: datetime.datetime) -> datetime.datetime:
        if self.output_config.roll_over_interval:
            interval = self.output_config.roll_over_interval.total_seconds()
            seconds = ((dt.hour * 60) + dt.minute) * 60 + dt.second
            partial = datetime.timedelta(seconds=seconds % interval,
                                         microseconds=dt.microsecond)
            boundary = dt - partial + datetime.timedelta(seconds=interval)
            return boundary
        else:
            return datetime.datetime.max

    def handle_write(self, stream_packets: bytes,
                     dt: datetime.datetime) -> None:
        if self.stop_time_target and dt > self.stop_time_target:
            # time to be done
            if not self.stop_time_reached:
                self.stop_time_reached = True
                self.close_compressor()

                if (self.schedule_item.failure_time and
                        dt > self.schedule_item.failure_time):
                    success = False
                else:
                    success = True

                try:
                    self.writer_status_callback.writer_stopped(
                        self.schedule_item.id, success)
                except Exception:
                    self.logger.exception(
                        "Exception in writer_stopped callback")
            else:
                return
        elif self.next_boundary is None:
            # first data point
            if (self.collection_time_target is None or
                    dt > self.collection_time_target):
                # time to start collecting
                self.collection_time_actual = dt
                self.calc_stop_time_target()
                self.next_boundary = self.calc_next_boundary(dt)
                self.open_compressor(dt)
            else:
                # not time yet
                return
        elif dt > self.next_boundary:
            # passed a boundary
            finished_filename = self.current_filename
            self.close_compressor()
            self.next_boundary = self.calc_next_boundary(dt)
            self.open_compressor(dt)
            self.mark_finished(finished_filename)

        if self.compressor_pipe:
            # write the bytes
            self.compressor_pipe.write(
                self.packet_leader_struct.pack(dt.timestamp(),
                                               len(stream_packets)))
            self.compressor_pipe.write(stream_packets)

    def write_loop(self) -> None:
        try:
            last_log = time.monotonic()
            slowdown_logged = False
            while True:
                try:
                    data = self.write_queue.get(True, 0.1)

                    # less than 100 elements is "empty"
                    qsize = self.write_queue.qsize()
                    now = time.monotonic()
                    if qsize >= 100:
                        if now - last_log >= 10.0:
                            slowdown_logged = True
                            msg = "Write queue slow down: %d elements"
                            self.logger.info(msg, qsize)
                            last_log = now
                    elif qsize == 0 and slowdown_logged:
                        slowdown_logged = False
                        self.logger.info("Write queue has caught up")
                        last_log = now

                    self.handle_write(*data)
                except Empty:
                    # check failure
                    if not self.stop_time_reached:
                        dt = datetime.datetime.now(datetime.timezone.utc)
                        if (self.schedule_item.failure_time and
                                dt > self.schedule_item.failure_time):
                            self.stop_time_reached = True
                            self.close_compressor()
                            try:
                                self.writer_status_callback.writer_stopped(
                                    self.schedule_item.id, False)
                            except Exception:
                                self.logger.exception(
                                    "Exception in writer callback")

                    if self.is_finished.is_set():
                        break
            finished_filename = self.current_filename
            self.close_compressor()
            self.mark_finished(finished_filename)
        except Exception:
            self.logger.exception("Uncaught exception in write_loop")
        finally:
            self.write_loop_exited.set()

    def monitor_loop(self) -> None:
        try:
            while True:
                try:
                    filename = self.finished_queue.get(True, 0.1)
                    with self.compressor_lock:
                        compressor = self.compressors.get(filename)
                    if compressor:
                        # there is a compressor for this file
                        ret_val = compressor.wait()
                        if ret_val != 0:
                            msg = "Compressor exited with error {}"
                            self.logger.warning(msg.format(ret_val))
                        with self.compressor_lock:
                            del self.compressors[filename]
                    # compressor is finished (or was None, e.g. internal lzma)
                    if self.output_config.upload_marker:
                        # empty out the .upload file
                        path, name = os.path.split(filename)
                        uploadfilename = os.path.join(
                            path, "." + name + UPLOAD_EXTENSION)

                        # NOTE: need to use r+ then truncate() on windows
                        # because of the hidden attribute. Windows doesn't like
                        # the 'w' mode on hidden files (need different flags
                        # passed to CreateFile).
                        with open(uploadfilename, 'r+',
                                  encoding="ascii") as uploadfile:
                            uploadfile.seek(0)
                            uploadfile.truncate()

                    # send notification
                    try:
                        self.writer_status_callback.writer_file_finished(
                            filename, self.schedule_item.id,
                            self.output_config.upload_marker)
                    except Exception:
                        self.logger.exception(
                            "Exception in writer_file_finished callback")
                except Empty:
                    if self.write_loop_exited.is_set():
                        break
            # write loop has exited, and finished queue is empty
            with self.compressor_lock:
                for filename, compressor in self.compressors.items():
                    ret_val = compressor.wait()
                    msg = "Uncollected compressor exited with code {}"
                    self.logger.warning(msg.format(ret_val))
                    try:
                        self.writer_status_callback.writer_file_finished(
                            filename, self.schedule_item.id,
                            self.output_config.upload_marker)
                    except Exception:
                        self.logger.exception(
                            "Exception in writer_file_finished exit callback")
                self.compressors.clear()
        except Exception:
            self.logger.exception("Uncaught exception in monitor_loop")

    def close(self) -> None:
        self.is_finished.set()

    def join(self) -> None:
        self.write_thread.join()
        self.monitor_thread.join()

    def update(self, schedule_item: ScheduleItem) -> None:
        if self.schedule_item == schedule_item:
            return  # nothing to do

        # NOTE: any exception here will closed the writer and open a new one
        if self.output_config != schedule_item.output_config:
            raise ValueError("Can't update output configuration while running")

        self.schedule_item = schedule_item
        self.collection_time_target = schedule_item.collection_time
        self.calc_stop_time_target()
