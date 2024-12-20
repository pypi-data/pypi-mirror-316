import logging
import multiprocessing
from multiprocessing.connection import Connection, wait
import threading
from typing import Callable, Optional, Protocol

import numpy
from numpy.typing import NDArray

from ..calc_process.types import ChannelInformation
from ..core.preferences import Preferences

logger = logging.getLogger(__name__)


DeviceCallback = Callable[[int, NDArray[numpy.float64]], None]


class ConnectivityHandler(Protocol):
    def stop_device(self, serial_number: str) -> None:
        ...

    def get_device_callback(self, serial_number: str,
                            channel_info: dict[int, ChannelInformation]
                            ) -> Optional[DeviceCallback]:
        ...

    def stop(self) -> None:
        ...

    def join(self) -> None:
        ...

    def update_preferences(self) -> None:
        ...


class ConnectivityManager:
    def __init__(self, preferences: Preferences):
        self.preferences = preferences

        self.stopped = False

        self.pipe_lock = threading.Lock()
        self.all_pipes: set[Connection] = set()
        self.pipe_callbacks: dict[Connection, list[DeviceCallback]] = {}
        self.device_pipes: dict[str, Connection] = {}

        self.pipe_thread_finished = threading.Event()
        self.pipe_thread = threading.Thread(target=self._pipe_loop)
        self.pipe_thread.start()

        self.handlers: list[ConnectivityHandler] = []

    def add_handler(self, handler: ConnectivityHandler) -> None:
        self.handlers.append(handler)

    def stop(self) -> None:
        # NOTE: the calc process may still be pushing data into pipes
        # so the pipe thread can't be stopped yet

        self.stopped = True

        # stop all handlers
        for handler in self.handlers:
            handler.stop()

        with self.pipe_lock:
            self.device_pipes.clear()
            self.pipe_callbacks.clear()

    def join(self) -> None:
        # NOTE: the calc process has been joined at this point

        # join all handlers
        for handler in self.handlers:
            handler.join()

        self.pipe_thread_finished.set()
        self.pipe_thread.join()

    def create_device_pipe(self, serial_number: str,
                           channel_info: dict[int, ChannelInformation]
                           ) -> Optional[Connection]:
        # clean up any old entries first
        self.stop_device(serial_number)

        if self.stopped:
            # we've already stopped
            return None

        callbacks: list[DeviceCallback] = []
        for handler in self.handlers:
            callback = handler.get_device_callback(serial_number, channel_info)
            if callback is not None:
                callbacks.append(callback)

        if not callbacks:
            return None

        device_rx_pipe, device_tx_pipe = multiprocessing.Pipe(False)

        with self.pipe_lock:
            device_pipe: Connection = device_rx_pipe  # type: ignore
            self.all_pipes.add(device_pipe)
            self.pipe_callbacks[device_pipe] = callbacks
            self.device_pipes[serial_number] = device_pipe

        return device_tx_pipe  # type: ignore

    def stop_device(self, serial_number: str) -> None:
        with self.pipe_lock:
            pipe = self.device_pipes.pop(serial_number, None)
            if pipe is not None:
                self.pipe_callbacks.pop(pipe, None)

        for handler in self.handlers:
            handler.stop_device(serial_number)

    def update_preferences(self) -> None:
        if self.stopped:
            # we've already stopped
            return

        for handler in self.handlers:
            handler.update_preferences()

    def _remove_pipe(self, pipe: Connection) -> None:  # call with pipe_lock
        self.all_pipes.discard(pipe)
        self.pipe_callbacks.pop(pipe, None)

        for serial_number, other_pipe in self.device_pipes.items():
            if pipe == other_pipe:
                del self.device_pipes[serial_number]
                break

    def _pipe_loop(self) -> None:
        try:
            while not self.pipe_thread_finished.is_set():
                with self.pipe_lock:
                    all_pipes_copy = list(self.all_pipes)

                if not all_pipes_copy:
                    self.pipe_thread_finished.wait(0.1)
                    continue

                ready: list[Connection] = wait(
                    all_pipes_copy, timeout=0.1)  # type: ignore

                with self.pipe_lock:
                    for pipe in ready:
                        try:
                            data: Optional[list[tuple[
                                int, NDArray[numpy.float64]]]] = pipe.recv()
                            if data is None:
                                # None signals that this pipe is done
                                self._remove_pipe(pipe)
                            else:
                                callbacks = self.pipe_callbacks.get(pipe)
                                if callbacks is not None:
                                    for value in data:
                                        for callback in callbacks:
                                            callback(*value)
                        except EOFError:
                            self._remove_pipe(pipe)
        except Exception:
            logger.exception("Uncaught exception in pipe_loop")
            self.stop()
