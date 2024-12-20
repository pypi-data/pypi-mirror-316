import itertools
import logging
from logging.handlers import QueueListener
import multiprocessing
import queue
import threading
import traceback
from typing import Any, Callable, Optional, ParamSpec, Union

from PySide6 import QtCore

import asphodel
from hyperborea.namedprocess import NamedProcess
from ..device_logging import DeviceLoggerAdapter, RemoteToLocalLogHandler
from .proxy_remote import (_simple_access, create_subproxy_util,
                           do_device_cleanup, FromProcessType, JobTuple,
                           proxy_process, TIMEOUT)

logger = logging.getLogger(__name__)


P = ParamSpec("P")


class DeviceOperation(QtCore.QObject):
    """
    This class represents an operation on the hardware (e.g. set_leds).
    """

    completed = QtCore.Signal(object)
    error = QtCore.Signal()  # no message; that's handled by the proxy's error

    def __init__(self, func: Callable, *args: Any, **kwargs: Any):
        super().__init__()
        self.func = func  # function to be called in the remote process
        self.args = args  # args to pass to the function
        self.kwargs = kwargs  # kwargs to pass to the function


class SimpleDeviceOperation(DeviceOperation):
    def __init__(self, function_name: str, *args: Any, **kwargs: Any):
        super().__init__(_simple_access, function_name, *args, **kwargs)


class DeviceProxy(QtCore.QObject):
    """
    This class represents a Device being handled in a different process.
    """

    connected = QtCore.Signal()
    disconnected = QtCore.Signal()
    error = QtCore.Signal(str)

    def __init__(self, proxy_manager: "DeviceProxyManager", process_name: str,
                 log_queue: "multiprocessing.Queue[Any]", serial_number: str,
                 proxy_string: str,
                 find_func: Callable[P, Optional[
                     asphodel.AsphodelNativeDevice]],
                 *args: P.args, **kwargs: P.kwargs) -> None:
        super().__init__()
        self.proxy_manager = proxy_manager
        self.serial_number = serial_number
        self.proxy_string = proxy_string
        self.log_queue = log_queue

        self.logger = DeviceLoggerAdapter(logger, serial_number, proxy_string)

        self.to_process_queue: "multiprocessing.Queue[Optional[JobTuple]]" = \
            multiprocessing.Queue()
        self.from_process_queue: \
            "multiprocessing.Queue[Optional[FromProcessType]]" = \
            multiprocessing.Queue()

        self.process = NamedProcess(
            name=process_name, description=serial_number, target=proxy_process,
            args=(self.log_queue, self.to_process_queue,
                  self.from_process_queue, serial_number, proxy_string,
                  find_func, args, kwargs))
        self.process.daemon = True

        self.monitor_thread = threading.Thread(target=self.monitor)

        self.job_lock = threading.Lock()
        self.jobs: dict[int, tuple[DeviceOperation, Proxy]] = {}
        self.next_job_index = 0

        self.subproxy_id_counter = itertools.count()

        self.logger.debug("Starting proxy")
        self.process.start()
        self.monitor_thread.start()

        # NOTE: connected is emitted when the device connection is established

    def handle_exception(self, proxy: "Proxy", exc: Exception) -> None:
        m = traceback.format_exception_only(type(exc), exc)
        message = "".join(m)

        # trim any trailing newline
        message = message.rstrip("\n")

        # already logged in the proxy process
        # proxy.logger.error(message)

        proxy.error.emit(message)
        proxy.close_connection()

    def handle_reply(self, reply: FromProcessType) -> None:
        try:
            if reply is True:  # connection success
                self.connected.emit()
            elif isinstance(reply, Exception):
                self.handle_exception(self, reply)
            else:
                job_id, result, exc = reply
                with self.job_lock:
                    operation, proxy = self.jobs.pop(job_id)
                if exc is None:
                    if result is None:  # NOTE: emitting None will crash pyside
                        result = type(None)  # send builtins.NoneType instead
                    del proxy
                    operation.completed.emit(result)
                else:
                    self.handle_exception(proxy, exc)
                    del proxy
                    operation.error.emit()
        except Exception:
            self.logger.exception("Unhandled Exception in Monitor Thread")

    def monitor(self) -> None:
        """
        thread target to monitor the responses from the remote process
        """
        self.logger.debug("Monitor thread starting")
        normal_exit = False
        while self.process.is_alive():  # check that process is still running
            try:
                reply = self.from_process_queue.get(True, TIMEOUT)
                if reply is None:  # check for sentinel value
                    normal_exit = True
                    break
                self.handle_reply(reply)
            except queue.Empty:
                pass
        # might still be entries in the queue
        while True:
            try:
                reply = self.from_process_queue.get(False)
                if reply is None:
                    normal_exit = True
                    continue
                self.handle_reply(reply)
            except queue.Empty:
                break
        with self.job_lock:
            for operation, _proxy in list(self.jobs.values()):
                operation.error.emit()
            self.jobs.clear()  # empty out the jobs
        self.logger.debug("Monitor thread finished")
        if not normal_exit:
            message = "Device Process Closed Prematurely!"
            self.logger.error(message)
            self.error.emit(message)
        self.disconnected.emit()
        self.process.join()
        self.from_process_queue.close()
        self.to_process_queue.close()
        self.logger.debug("Monitor thread closing")

    def close_connection(self) -> None:
        # NOTE: may be called from monitor thread or main thread
        # NOTE: monitor waits for process to finish then emits disconnected
        try:
            self.to_process_queue.put(None)  # send sentinel value
        except ValueError:
            pass  # monitor thread exited and queue is already closed

    def send_job(self, operation: DeviceOperation, *args: Any,
                 subproxy: Optional["DeviceSubProxy"] = None,
                 **kwargs: Any) -> None:
        # NOTE: may be called from monitor thread or main thread
        proxy: Proxy
        if subproxy is None:
            proxy = self
            subproxy_id = None
        else:
            proxy = subproxy
            subproxy_id = subproxy.subproxy_id

        with self.job_lock:
            job_index = self.next_job_index
            self.next_job_index = (self.next_job_index + 1) & 0xFFFFFFFF
            self.jobs[job_index] = (operation, proxy)

        new_kwargs = dict(list(operation.kwargs.items()) +
                          list(kwargs.items()))
        new_args = operation.args + args

        job: JobTuple = (job_index, subproxy_id, operation.func, new_args,
                         new_kwargs)
        try:
            self.to_process_queue.put(job)
        except ValueError:
            self.logger.warning("Sending job after monitor thread has exited")
            operation.error.emit()

    def wait_for_close(self) -> None:
        if self.monitor_thread.is_alive():
            self.close_connection()
            self.monitor_thread.join()

    def is_finished(self) -> bool:
        return not self.monitor_thread.is_alive()

    def create_subproxy(self, func: Callable, *args: Any,
                        **kwargs: Any) -> "DeviceSubProxy":
        subproxy_id = next(self.subproxy_id_counter)
        op = DeviceOperation(create_subproxy_util, func, subproxy_id,
                             self.proxy_string, *args, **kwargs)
        subproxy = DeviceSubProxy(self, subproxy_id, op)
        self.proxy_manager.proxies.append(subproxy)
        return subproxy


class DeviceSubProxy(QtCore.QObject):

    connected = QtCore.Signal()
    disconnected = QtCore.Signal()
    error = QtCore.Signal(str)

    def __init__(self, proxy: DeviceProxy, subproxy_id: int,
                 start_op: DeviceOperation):
        super().__init__()

        self.proxy = proxy
        self.logger = proxy.logger  # temporary until we get a new one
        self.subproxy_id = subproxy_id
        start_op.completed.connect(self._connected_cb)

        self.closed = False
        self.closed_finished = False

        # connect signals from the parent into this instance
        self.proxy.disconnected.connect(self.disconnected)
        self.proxy.error.connect(self.error)

        self.close_job = DeviceOperation(do_device_cleanup)
        self.close_job.completed.connect(self.close_completed)
        self.close_job.error.connect(self.close_completed)

        self.logger.debug("Starting subproxy")
        self.proxy.send_job(start_op)

        # NOTE: connected is emitted when the device connection is established

    def close_connection(self) -> None:
        # NOTE: may be called from monitor thread or main thread
        if not self.closed:
            self.closed = True
            self.proxy.send_job(self.close_job, subproxy=self)

    @QtCore.Slot()
    def close_completed(self) -> None:
        self.proxy.disconnected.disconnect(self.disconnected)
        self.proxy.error.disconnect(self.error)
        self.disconnected.emit()
        self.closed_finished = True

    @QtCore.Slot(object)
    def _connected_cb(self, result: Optional[tuple[str, str]]) -> None:
        if result is not None:
            serial_number, subproxy_string = result
            self.logger = DeviceLoggerAdapter(logger, serial_number,
                                              subproxy_string)
            self.connected.emit()
        else:
            self.error.emit("Subproxy Creation Failed")
            self.proxy.disconnected.disconnect(self.disconnected)
            self.proxy.error.disconnect(self.error)
            self.disconnected.emit()

    def wait_for_close(self) -> None:
        pass  # nothing to do in a subproxy

    def is_finished(self) -> bool:
        return self.closed_finished

    def send_job(self, operation: DeviceOperation, *args: Any,
                 **kwargs: Any) -> None:
        self.proxy.send_job(operation, *args, subproxy=self, **kwargs)


Proxy = Union[DeviceProxy, DeviceSubProxy]


class DeviceProxyManager:
    def __init__(self, process_name: str):
        self.process_name = process_name
        self.setup_logging()
        self.proxies: list[Proxy] = []
        self.next_proxy_number = 0

    def setup_logging(self) -> None:
        local_handler = RemoteToLocalLogHandler(__name__ + ".remote")

        self.log_queue: "multiprocessing.Queue[Any]" = multiprocessing.Queue()
        self.log_listener = QueueListener(self.log_queue, local_handler)
        self.log_listener.start()

    def stop(self) -> None:
        for proxy in self.proxies:
            proxy.close_connection()
        for proxy in self.proxies:
            proxy.wait_for_close()
        self.log_listener.stop()

    def clear_finished_proxies(self) -> None:
        for proxy in self.proxies.copy():
            if proxy.is_finished():
                self.proxies.remove(proxy)

    def new_proxy(self, serial_number: str,
                  find_func: Callable[P, Optional[
                      asphodel.AsphodelNativeDevice]],
                  *args: P.args, **kwargs: P.kwargs) -> DeviceProxy:
        proxy_number = self.next_proxy_number
        self.next_proxy_number += 1

        proxy_string = "{}:{}".format(proxy_number, serial_number)

        proxy = DeviceProxy(
            self, self.process_name, self.log_queue, serial_number,
            proxy_string, find_func, *args, **kwargs)
        self.proxies.append(proxy)
        return proxy
