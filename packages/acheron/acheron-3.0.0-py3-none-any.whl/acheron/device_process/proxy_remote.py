import logging
from logging.handlers import QueueHandler
import multiprocessing
import os
import queue
import signal
import sys
import threading
from typing import Any, Callable, cast, Literal, Optional, Union

import psutil

from asphodel import AsphodelNativeDevice

from ..device_logging import DeviceLoggerAdapter

logger = logging.getLogger(__name__)


TIMEOUT = 0.1  # 100 milliseconds

CleanupTuple = tuple[Callable, tuple, dict]
JobTuple = tuple[int, Optional[int], Callable, tuple, dict]
JobReplyTuple = tuple[int, Any, Optional[Exception]]
FromProcessType = Union[Literal[True], JobReplyTuple, Exception]

# globals
# value: list of (func, [args], {kwargs})
device_cleanup: dict[Optional[AsphodelNativeDevice], list[CleanupTuple]] = {}
device_lock = threading.Lock()
subproxy_devices: dict[Optional[int], AsphodelNativeDevice] = {}

# value: (serial_number, proxy_string)
device_identifiers: dict[AsphodelNativeDevice, tuple[str, str]] = {}


def _simple_access(device: AsphodelNativeDevice, function_name: str,
                   *args: Any, **kwargs: Any) -> Any:
    func = getattr(device, function_name)
    result = func(*args, **kwargs)
    return result


def get_device_logger(
        logger: logging.Logger,
        device: Optional[AsphodelNativeDevice]) -> DeviceLoggerAdapter:
    serial_number, proxy_string = device_identifiers.get(
        device, ("unknown", "unknown"))  # type: ignore
    return DeviceLoggerAdapter(logger, serial_number, proxy_string)


def setup_remote_logging(log_queue: "multiprocessing.Queue[Any]") -> None:
    handler = QueueHandler(log_queue)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)
    # remove pyusb's logging info
    pyusb_logger = logging.getLogger("usb")
    pyusb_logger.propagate = False


def register_device_cleanup(device: Optional[AsphodelNativeDevice],
                            cleanup_func: Callable, *args: Any,
                            **kwargs: Any) -> None:
    cleanup_list = device_cleanup.setdefault(device, [])
    cleanup_list.append((cleanup_func, args, kwargs))


def unregister_device_cleanup(device: Optional[AsphodelNativeDevice],
                              cleanup_func: Callable, *args: Any,
                              **kwargs: Any) -> None:
    cleanup_list = device_cleanup.get(device, None)
    if cleanup_list:
        try:
            cleanup_list.remove((cleanup_func, args, kwargs))
        except ValueError:
            pass  # was already removed

        if not cleanup_list:
            # last one was just removed
            del device_cleanup[device]


def do_device_cleanup(device: Optional[AsphodelNativeDevice]) -> None:
    cleanup_list = device_cleanup.pop(device, [])
    for cleanup in cleanup_list:
        try:
            func, args, kwargs = cleanup
            func(device, *args, **kwargs)
        except Exception:
            device_logger = get_device_logger(logger, device)
            device_logger.exception("Exception during cleanup")


def do_final_cleanup(device: Optional[AsphodelNativeDevice]) -> None:
    # do subproxy cleanup first
    subproxy_devices = set(device_cleanup.keys())
    subproxy_devices.discard(device)
    subproxy_devices.discard(None)
    for subproxy_device in subproxy_devices:
        do_device_cleanup(subproxy_device)

    # do device cleanup
    do_device_cleanup(device)

    # do final cleanup
    do_device_cleanup(None)


def proxy_process(
        log_queue: "multiprocessing.Queue[Any]",
        incoming: "multiprocessing.Queue[Optional[JobTuple]]",
        outgoing: "multiprocessing.Queue[Optional[FromProcessType]]",
        serial_number: str, proxy_string: str, find_func: Callable,
        ffargs: tuple, ffkwargs: dict) -> None:

    # fix a bug with stderr and stdout being None
    sys.stdout = open(os.devnull)
    sys.stderr = open(os.devnull)

    setup_remote_logging(log_queue)

    device = None

    # create a logger using the device specific identifier
    device_logger = DeviceLoggerAdapter(logger, serial_number, proxy_string)

    # ctrl+c handling: want to let the main process send the exit command
    if sys.platform == "win32":
        # the best way on windows? since we can't create a new process group
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    else:
        # move to a new process group (won't be signalled with ctrl+c)
        os.setpgrp()

    arg_strs = [repr(x) for x in ffargs]
    arg_strs.extend("{}={}".format(k, repr(v)) for k, v in ffkwargs.items())
    find_func_str = "{}({})".format(find_func.__name__, ", ".join(arg_strs))
    device_logger.debug("Proxy process starting with %s", find_func_str)

    me = psutil.Process(os.getpid())
    try:
        try:
            device = cast(Optional[AsphodelNativeDevice],
                          find_func(*ffargs, **ffkwargs))
            outgoing.put(True)  # signals success
        except Exception as e:
            device_logger.exception("Exception")
            outgoing.put(e)
        device_logger.debug("Proxy running")
        if device:
            subproxy_devices[None] = device
            device_identifiers[device] = (serial_number, proxy_string)
            while True:
                parent = me.parent()
                if parent is None or not parent.is_running():
                    break

                try:
                    job: Optional[JobTuple] = incoming.get(True, TIMEOUT)
                    if job is None:  # check for sentinel value
                        break
                    job_id, subproxy_id, func, args, kwargs = job
                    with device_lock:
                        proxy_device = subproxy_devices[subproxy_id]
                        proxy_logger = get_device_logger(logger, proxy_device)
                        proxy_logger.debug("got: {}".format(job))
                        outgoing_tuple: JobReplyTuple
                        try:
                            result = func(proxy_device, *args, **kwargs)
                            outgoing_tuple = (job_id, result, None)
                            msg = "finished: {} => {}".format(job, result)
                            proxy_logger.debug(msg)
                        except Exception as e:
                            proxy_logger.exception("Exception")
                            outgoing_tuple = (job_id, None, e)
                        outgoing.put(outgoing_tuple)
                except queue.Empty:
                    pass

        # finished with the outgoing queue
        outgoing.put(None)  # sentinel value
        outgoing.close()

        if device:
            with device_lock:
                do_final_cleanup(device)
    except Exception:
        device_logger.exception("Uncaught Exception in Remote Process")
        raise
    finally:
        if device:
            device.close()
    device_logger.debug("Proxy process ending")


def create_subproxy_util(
        device: AsphodelNativeDevice, func: Callable, subproxy_id: int,
        proxy_string: str, *args: Any,
        **kwargs: Any) -> Optional[tuple[str, str]]:
    """ called from create_subproxy() to handle registration """
    try:
        subproxy_device = func(device, *args, **kwargs)
        subproxy_devices[subproxy_id] = subproxy_device

        subproxy_sn = subproxy_device.get_serial_number()
        subproxy_string = "{}->{}".format(proxy_string, subproxy_sn)
        device_identifiers[subproxy_device] = (subproxy_sn, subproxy_string)

        return (subproxy_sn, subproxy_string)
    except Exception:
        get_device_logger(logger, device).exception(
            "Unhandled exception in create_subproxy_util()")
        return None
