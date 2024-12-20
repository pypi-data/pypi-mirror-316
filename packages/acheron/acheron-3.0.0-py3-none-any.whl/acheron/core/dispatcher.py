from collections import deque
import datetime
import functools
import logging
import os
import queue
import threading
from typing import Any, Callable, Optional, ParamSpec
import urllib.parse
import urllib.request
import weakref
from weakref import ReferenceType

import diskcache
from PySide6 import QtCore

import asphodel
from ..device_process.proxy import DeviceProxyManager, DeviceSubProxy, Proxy

from .device_controller import DeviceController, RFPowerStatus
from .main_schedule import MainSchedule
from .preferences import Preferences
from .radio_scan import ActiveScanDatabase
from ..calc_process.runnner import CalcProcess
from ..connectivity.alert_emailer import AlertEmailManager
from ..connectivity.connectivity_manager import ConnectivityManager
from ..connectivity.event_upload import EventUploader
from ..connectivity.modbus import ModbusHandler
from ..connectivity.s3upload import mark_file_for_upload, S3UploadManager
from ..connectivity.socket_handler import SocketHandler
from ..device_process.remote_funcs import (
    connect_and_open_tcp_device, find_and_open_tcp_device,
    find_and_open_usb_device)

logger = logging.getLogger(__name__)


P = ParamSpec("P")


class Dispatcher(QtCore.QObject):
    controller_created = QtCore.Signal(object)
    controller_stopped = QtCore.Signal(object)

    rf_power_changed = QtCore.Signal(int, int)  # enabled, total

    active_triggers_changed = QtCore.Signal(object)  # set of trigger ids

    # NOTE: this is a weird one. It's called when the initial devices are
    # connected, if any. If a TCP scan was performed, the first argument is
    # True, and the second is a possibly empty list of TCP devices.
    # If no TCP scan was performed, the first argument is False and the second
    # is an empty list, as QT doesn't allow passing None in signals
    initial_devices_connected = QtCore.Signal(bool, object)  # list of devices

    upload_manager_changed = QtCore.Signal(object)

    _create_signal = QtCore.Signal(object)
    _cleanup = QtCore.Signal(object)

    def __init__(self, proxy_manager: DeviceProxyManager,
                 preferences: Preferences, calc_process_name: str):
        super().__init__()

        self.proxy_manager = proxy_manager
        self.preferences = preferences
        self.calc_process_name = calc_process_name

        self.disable_streaming = self.preferences.disable_streaming
        self.disable_archiving = self.preferences.disable_archiving

        self.alert_manager = AlertEmailManager(self.preferences)

        self.upload_manager: Optional[S3UploadManager] = None
        self.upload_options: Optional[dict[str, Any]] = None

        self.event_uploader = EventUploader(self.preferences)

        self.main_schedule = MainSchedule()

        self.diskcache = diskcache.Cache(
            self.preferences.diskcache_dir, size_limit=100e6)

        self.active_scan_database = ActiveScanDatabase(self.preferences)

        self.lock = threading.Lock()

        # all of these are locked
        self.proxies: dict[Proxy, str] = {}  # value is location
        self.opening_proxies: set[Proxy] = set()  # for GC
        self.controllers: dict[tuple[str, ...], DeviceController] = {}
        self.controller_info: dict[DeviceController, dict] = {}
        self.disconnected_controllers: set[DeviceController] = set()
        self.manually_disconnected: set[tuple[str, ...]] = set()
        self.rf_power_statuses: dict[DeviceController, RFPowerStatus] = {}
        self.rf_power_needed: set[DeviceController] = set()
        self.controller_active_triggers: dict[DeviceController,
                                              frozenset[str]] = {}
        self.active_triggers: frozenset[str] = frozenset()

        self.updating_rf = False

        self.finished = threading.Event()
        self.controller_connect_queue: queue.Queue[dict] = queue.Queue()
        self.background_connect_thread = threading.Thread(
            target=self.background_connect_loop)

        self.final_join = threading.Event()
        self.background_join_deque: deque[Callable[[], None]] = deque()
        self.background_join_thread = threading.Thread(
            target=self._background_join_run)
        self.background_join_thread.start()

        self.create_upload_manager()
        self.create_connectivity_manager()

        self.setup_callbacks()

        # schedule the initial connect for the beginning of the main loop
        QtCore.QTimer.singleShot(0, self.initial_device_connect)

    def setup_callbacks(self) -> None:
        self._create_signal.connect(self._create_cb)
        self._cleanup.connect(self._cleanup_cb)

    def stop(self) -> None:
        with self.lock:
            controllers = list(self.controllers.values())
            self.opening_proxies.clear()

        # stop all controllers (parents first)
        stopped = set()
        for controller in controllers:
            if controller in stopped:
                continue
            parent = controller.parent_controller
            if parent is not None and parent not in stopped:
                parent.stop()
                parent.join()
                self.controller_stopped.emit(parent)
                stopped.add(parent)
            controller.stop()
            controller.join()
            self.controller_stopped.emit(controller)
            stopped.add(controller)

        # clear out the controller data structures
        with self.lock:
            self.controllers.clear()
            self.rf_power_statuses.clear()
            self.rf_power_needed.clear()
            self.controller_active_triggers.clear()
            self.active_triggers = frozenset()
            self.controller_info.clear()
            self.disconnected_controllers.clear()

        # stop the threads
        self.finished.set()

        if self.upload_manager:
            self.upload_manager.stop()
            self.background_join_deque.append(self.upload_manager.join)
            self.upload_manager = None

        self.alert_manager.stop()

        self.connectivity_manager.stop()
        self.event_uploader.stop()

    def join(self) -> None:
        self.final_join.set()

        self.background_connect_thread.join()

        self.background_join_thread.join()

        self.connectivity_manager.join()
        self.event_uploader.join()

    @QtCore.Slot(object)
    def _cleanup_cb(self, joined: list) -> None:
        joined.clear()

        # do this just because we can
        self.proxy_manager.clear_finished_proxies()

    def _do_join_pass(self) -> list[Callable[[], None]]:
        joined: list[Callable[[], None]] = []
        while self.background_join_deque:
            join_func = self.background_join_deque.popleft()
            try:
                join_func()
            except Exception:
                logger.exception("Failed to join %s", join_func)
            joined.append(join_func)
        return joined

    def _background_join_run(self) -> None:
        while not self.final_join.wait(timeout=0.1):
            joined = self._do_join_pass()

            if joined:
                # finish up things in the main thread to avoid race conditions
                self._cleanup.emit(joined)
                del joined

        # do one final pass
        self._do_join_pass()

        logger.debug("Background join thread exiting")

    def create_upload_manager(self) -> None:
        if self.preferences.upload_enabled:
            upload_options = {
                'base_dir': self.preferences.base_dir,
                's3_bucket': self.preferences.s3_bucket,
                'key_prefix': self.preferences.upload_directory,
                'access_key_id': self.preferences.access_key_id,
                'secret_access_key': self.preferences.secret_access_key,
                'aws_region': self.preferences.aws_region,
                'delete_after_upload': self.preferences.delete_original,
                'archive_interval': datetime.timedelta(
                    minutes=self.preferences.archive_interval),
            }
        else:
            upload_options = None

        if upload_options == self.upload_options:
            # No change
            return

        self.upload_options = upload_options

        if self.upload_manager:
            self.upload_manager.stop()
            self.background_join_deque.append(self.upload_manager.join)
            self.upload_manager = None

        if upload_options:
            try:
                self.upload_manager = S3UploadManager(**upload_options)
            except Exception:
                msg = "Error starting uploader. Check upload configuration."
                logger.exception(msg)

        self.upload_manager_changed.emit(self.upload_manager)

    def create_connectivity_manager(self) -> None:
        self.connectivity_manager = ConnectivityManager(self.preferences)
        self.connectivity_manager.add_handler(SocketHandler(self.preferences))
        self.connectivity_manager.add_handler(ModbusHandler(self.preferences))

    @QtCore.Slot(object)
    def _create_cb(self, f: Callable) -> None:
        f()

    def _start_proxy(self, proxy: Proxy, controller: DeviceController) -> None:
        # use a weakref in the partial to allow GC
        connected = functools.partial(
            self._proxy_connected, weakref.ref(proxy), weakref.ref(controller))
        proxy.connected.connect(connected)

        # use a weakref in the partial to allow GC
        disconnected = functools.partial(
            self._proxy_disconnected, weakref.ref(proxy),
            weakref.ref(controller))
        proxy.disconnected.connect(disconnected)

        self.opening_proxies.add(proxy)

    def _create_proxy(self, serial_number: str, location: str,
                      reconnect_info: dict,
                      find_func: Callable[P, Optional[
                          asphodel.AsphodelNativeDevice]],
                      *args: P.args, **kwargs: P.kwargs) -> None:
        # create the controller now so proxy errors get shown to the user
        controller = self._update_or_create_controller(
            (serial_number,), None, reconnect_info, None, set())

        proxy = self.proxy_manager.new_proxy(serial_number, find_func, *args,
                                             **kwargs)
        with self.lock:
            self.proxies[proxy] = location

        self._start_proxy(proxy, controller)

    def _proxy_connected(
            self, proxy_ref: "ReferenceType[Proxy]",
            controller_ref: "ReferenceType[DeviceController]") -> None:
        proxy = proxy_ref()
        controller = controller_ref()

        if proxy is not None and controller is not None:
            controller.set_proxy(proxy)

        with self.lock:
            if proxy is not None:
                self.opening_proxies.discard(proxy)
            if controller is not None:
                self.disconnected_controllers.discard(controller)

    def _proxy_disconnected(
            self, proxy_ref: "ReferenceType[Proxy]",
            controller_ref: "ReferenceType[DeviceController]") -> None:
        proxy = proxy_ref()
        controller = controller_ref()

        # NOTE: controller handles its own disconnect

        # remove the proxy from the proxies list
        with self.lock:
            if proxy is not None:
                self.opening_proxies.discard(proxy)
                try:
                    del self.proxies[proxy]
                except KeyError:
                    pass

            if controller is not None:
                if controller in self.controllers.values():
                    self.disconnected_controllers.add(controller)

    def get_proxy_locations(self) -> set[str]:
        with self.lock:
            return set(self.proxies.values())

    def create_usb_proxy(self, serial_number: str, location: str) -> None:
        reconnect_info = {
            "type": "usb",
            "location": location,
            "serial_number": serial_number,
        }
        self._create_proxy(serial_number, location, reconnect_info,
                           find_and_open_usb_device, location)

    def create_tcp_proxy(self, serial_number: str, location: str) -> None:
        reconnect_info = {
            "type": "tcp",
            "location": location,
            "serial_number": serial_number,
        }
        self._create_proxy(serial_number, location, reconnect_info,
                           find_and_open_tcp_device, serial_number, location)

    def create_tcp_proxy_from_device(
            self, tcp_device: asphodel.AsphodelNativeDevice) -> None:
        adv = tcp_device.tcp_get_advertisement()
        serial_number = adv.serial_number
        location = tcp_device.get_location_string()
        self.create_tcp_proxy(serial_number, location)

    def create_manual_tcp_proxy(self, hostname: str, port: int, timeout: int,
                                serial_number: Optional[str],
                                err_cb: Optional[Callable]) -> None:
        manual_tcp_info = {
            "hostname": hostname,
            "port": port,
            "timeout": timeout,
            "serial_number": serial_number,
            "err_cb": err_cb,
        }
        # push info to queue
        self.controller_connect_queue.put(manual_tcp_info)

    def _collect_new_usb_device_keys(self, locations: set[str]) \
            -> set[tuple[str, str]]:
        keys: set[tuple[str, str]] = set()
        for device in asphodel.find_usb_devices():
            location: str = device.get_location_string()
            if location not in locations:
                # found one we don't already have
                try:
                    device.open()
                    serial_number: str = device.get_serial_number()
                except asphodel.AsphodelError:
                    continue
                finally:
                    device.close()

                keys.add((serial_number, location))
        return keys

    def _collect_new_tcp_device_keys(self, locations: set[str]) \
            -> set[tuple[str, str]]:
        keys: set[tuple[str, str]] = set()
        for device in asphodel.find_tcp_devices():
            adv = device.tcp_get_advertisement()
            if adv.connected:
                continue
            location: str = device.get_location_string()
            serial_number = adv.serial_number
            if location not in locations:
                keys.add((serial_number, location))
        return keys

    @QtCore.Slot()
    def rescan_usb(self) -> None:
        if not asphodel.nativelib.usb_devices_supported:
            return

        locations = self.get_proxy_locations()
        usb_keys = self._collect_new_usb_device_keys(locations)
        for serial_number, location in usb_keys:
            self.create_usb_proxy(serial_number, location)

    @QtCore.Slot()
    def initial_device_connect(self) -> None:
        # fix a problem with the TCP connection dialog not being displayed in
        # the correct location, probably related to QTBUG-106678
        QtCore.QCoreApplication.processEvents()

        tcp_scanned = False
        tcp_devices: list[asphodel.AsphodelNativeDevice] = []

        if (self.preferences.initial_connect_usb or
                self.preferences.rescan_connect_usb):
            self.rescan_usb()

        if (self.preferences.initial_connect_tcp or
                self.preferences.rescan_connect_tcp):
            if asphodel.nativelib.tcp_devices_supported:
                tcp_devices = asphodel.find_tcp_devices()
                tcp_scanned = True

                locations = self.get_proxy_locations()
                for device in tcp_devices:
                    adv = device.tcp_get_advertisement()
                    if adv.connected:
                        continue
                    serial_number = adv.serial_number
                    location: str = device.get_location_string()
                    if location not in locations:
                        logger.debug("Connecting TCP device %s", serial_number)
                        self.create_tcp_proxy(serial_number, location)

        create: set[str] = set()
        with self.lock:
            for serial_number in self.preferences.initial_serials:
                serial_number = serial_number.strip()
                if not serial_number:
                    continue

                if serial_number not in self.controllers:
                    create.add(serial_number)

        for serial_number in create:
            controller = self._update_or_create_controller(
                (serial_number,), None, None, None, set())
            with self.lock:
                self.disconnected_controllers.add(controller)

        self.initial_devices_connected.emit(tcp_scanned, tcp_devices)

        self.background_connect_thread.start()

    def _update_or_create_controller(
            self,
            serial_numbers: tuple[str, ...],
            proxy: Optional[Proxy],
            reconnect_info: Optional[dict],
            parent_controller: Optional[DeviceController],
            parties: set[str]) -> DeviceController:
        # NOTE: may return an existing controller for this serial number
        with self.lock:
            controller = self.controllers.get(serial_numbers)
            if not controller:
                logger.debug("Creating device controller for %s",
                             serial_numbers)
                schedule = self.main_schedule.get_schedule(serial_numbers)
                controller = DeviceController(
                    self, serial_numbers[-1], self.preferences, self.diskcache,
                    schedule, self.calc_process_name, self.disable_streaming,
                    self.disable_archiving, parent_controller, parties)
                controller.rf_power_changed.connect(self.rf_power_changed_cb)
                controller.rf_power_needed.connect(self.rf_power_needed_cb)
                controller.active_triggers_changed.connect(
                    self.active_triggers_changed_cb)

                # active scan database callbacks
                controller.disconnected_signal.connect(
                    self.active_scan_database.controller_disconnected)
                controller.remote_connecting.connect(
                    self.active_scan_database.controller_remote_connecting)
                controller.scan_data.connect(
                    self.active_scan_database.controller_scans)
                controller.active_scan_data.connect(
                    self.active_scan_database.active_scan_finished)

                self.controllers[serial_numbers] = controller

                self.manually_disconnected.discard(serial_numbers)

                created = True
            else:
                created = False
                if parties:
                    controller.register_parties(parties)

            if proxy:
                controller.set_proxy(proxy)
                self.disconnected_controllers.discard(controller)
            elif created:
                self.disconnected_controllers.add(controller)

            if reconnect_info:
                self.controller_info[controller] = reconnect_info

        if created:
            self.controller_created.emit(controller)

        return controller

    def stop_controller(self, controller: DeviceController) -> None:
        children: list[DeviceController] = []
        with self.lock:
            for c in self.controllers.values():
                if c.parent_controller == controller:
                    children.append(c)

        for child in children:
            self.stop_controller(child)

        controller.stop()

        last_power_needed = False

        with self.lock:
            serial_number_tuples: set[tuple[str, ...]] = set()
            for serial_numbers, c in self.controllers.items():
                if c == controller:
                    serial_number_tuples.add(serial_numbers)

            for serial_numbers in serial_number_tuples:
                del self.controllers[serial_numbers]

            try:
                del self.controller_info[controller]
            except KeyError:
                pass

            try:
                del self.rf_power_statuses[controller]
            except KeyError:
                pass

            if self.rf_power_needed:
                self.rf_power_needed.discard(controller)
                if not self.rf_power_needed:
                    last_power_needed = True

            self.disconnected_controllers.discard(controller)

        if last_power_needed:
            self.disable_all_rf_power()

        # this is a simple way to update triggers correctly
        self.active_triggers_changed_cb(controller, frozenset())

        self.controller_stopped.emit(controller)

        if controller.parent_controller:
            party = f"parent-{controller.serial_number}"
            controller.parent_controller.release_party(party)

        self.background_join_deque.append(controller.join)

    def _check_reconnect_devices(self) -> None:
        rescan_connect_usb = self.preferences.rescan_connect_usb
        rescan_connect_tcp = self.preferences.rescan_connect_tcp

        scan_usb = rescan_connect_usb  # initial value
        scan_tcp = rescan_connect_tcp  # initial value

        with self.lock:
            locations = set(self.proxies.values())
            for controller in self.disconnected_controllers:
                reconnect_info = self.controller_info.get(controller)

                if reconnect_info is None:
                    # device has never been connected before, look everywhere
                    scan_usb = True
                    scan_tcp = True
                    continue

                reconnect_type = reconnect_info['type']
                if reconnect_type == "usb":
                    scan_usb = True
                elif reconnect_type == "tcp":
                    scan_tcp = True
                elif reconnect_type == "manual_tcp":
                    if reconnect_info['location'] not in locations:
                        manual_tcp_info = {
                            "hostname": reconnect_info["hostname"],
                            "port": reconnect_info["port"],
                            "timeout": reconnect_info["timeout"],
                            "serial_number": reconnect_info["serial_number"],
                            "err_cb": None,
                        }
                        self.controller_connect_queue.put(manual_tcp_info)

        if scan_usb and asphodel.nativelib.usb_devices_supported:
            usb_keys = self._collect_new_usb_device_keys(locations)
        else:
            usb_keys = set()

        if scan_tcp and asphodel.nativelib.tcp_devices_supported:
            tcp_keys = self._collect_new_tcp_device_keys(locations)
        else:
            tcp_keys = set()

        create_funcs = []
        with self.lock:
            for serial_number, location in usb_keys:
                c = self.controllers.get((serial_number,))
                if c and c in self.disconnected_controllers:
                    add = True
                elif c is None and rescan_connect_usb:
                    add = serial_number not in self.manually_disconnected
                else:
                    add = False

                if add:
                    f = functools.partial(
                        self.create_usb_proxy, serial_number, location)
                    create_funcs.append(f)

            for serial_number, location in tcp_keys:
                c = self.controllers.get((serial_number,))
                if c and c in self.disconnected_controllers:
                    add = True
                elif c is None and rescan_connect_tcp:
                    add = serial_number not in self.manually_disconnected
                else:
                    add = False

                if add:
                    f = functools.partial(
                        self.create_tcp_proxy, serial_number, location)
                    create_funcs.append(f)

        # create the new proxies outside of the lock
        for f in create_funcs:
            self._create_signal.emit(f)

    def _connect_manual_tcp_proxy(self, hostname: str, port: int, timeout: int,
                                  serial_number: Optional[str],
                                  err_cb: Optional[Callable]) -> None:
        try:
            device = asphodel.create_tcp_device(hostname, port, timeout,
                                                serial_number)
        except asphodel.AsphodelError:
            logger.exception("Could not connect to TCP device.")
            if err_cb:
                err_cb()
            return

        adv = device.tcp_get_advertisement()
        found_serial_number = adv.serial_number
        location = device.get_location_string()

        reconnect_info = {
            "type": "manual_tcp",
            "location": location,
            "serial_number": found_serial_number,
            "hostname": hostname,
            "port": port,
            "timeout": timeout,
        }

        f = functools.partial(
            self._create_proxy, found_serial_number, location, reconnect_info,
            connect_and_open_tcp_device, hostname, port, timeout,
            found_serial_number)

        self._create_signal.emit(f)

    def background_connect_loop(self) -> None:
        try:
            while True:
                if self.finished.is_set():
                    break

                self._check_reconnect_devices()

                while True:
                    try:
                        # 1.5 second wait time
                        manual_tcp_info = self.controller_connect_queue.get(
                            True, 1.5)
                        self._connect_manual_tcp_proxy(**manual_tcp_info)
                    except queue.Empty:
                        break
        except Exception:
            logger.exception("Uncaught exception in background_connect_loop")

    def set_disable_streaming(self, disable: bool) -> None:
        with self.lock:
            self.disable_streaming = disable  # record for future controllers
            for controller in self.controllers.values():
                controller.update_disable_streaming(disable)

    def set_disable_archiving(self, disable: bool) -> None:
        with self.lock:
            self.disable_archiving = disable  # record for future controllers
            for controller in self.controllers.values():
                controller.update_disable_archiving(disable)

    def mark_for_upload(self, files: list[str]) -> None:
        if len(files) == 0:
            return

        for filename in files:
            logger.info("Marking file {}".format(filename))
            mark_file_for_upload(filename)

        if self.upload_manager:
            self.upload_manager.rescan()

    def update_preferences(self) -> None:
        with self.lock:
            controller_copy = self.controllers.copy()

        for controller in controller_copy.values():
            controller.update_preferences()

        # this function will handle checking for changes
        self.create_upload_manager()

        self.alert_manager.update_preferences()

        self.connectivity_manager.update_preferences()

    def _emit_rf_power_status(self) -> None:
        self.rf_power_changed.emit(*self.get_rf_power_status())

    def get_rf_power_status(self) -> tuple[int, int]:
        enabled = 0
        total = 0
        with self.lock:
            for status in self.rf_power_statuses.values():
                if status == RFPowerStatus.ENABLED:
                    enabled += 1
                total += 1
        return enabled, total

    @QtCore.Slot(object, object)
    def rf_power_changed_cb(self, controller: DeviceController,
                            status: RFPowerStatus) -> None:
        with self.lock:
            if status == RFPowerStatus.NOT_SUPPORTED:
                try:
                    del self.rf_power_statuses[controller]
                except KeyError:
                    pass
            else:
                self.rf_power_statuses[controller] = status

        if not self.updating_rf:
            self._emit_rf_power_status()

    @QtCore.Slot()
    def enable_all_rf_power(self) -> None:
        self.updating_rf = True
        with self.lock:
            all_controllers = set(self.controllers.values())
        for controller in all_controllers:
            controller.enable_rf_power()
        self.updating_rf = False

        self._emit_rf_power_status()

    @QtCore.Slot()
    def disable_all_rf_power(self) -> None:
        self.updating_rf = True
        with self.lock:
            all_controllers = set(self.controllers.values())
        for controller in all_controllers:
            controller.disable_rf_power()
        self.updating_rf = False

        self._emit_rf_power_status()

    @QtCore.Slot(object, bool)
    def rf_power_needed_cb(self, controller: DeviceController,
                           needed: bool) -> None:
        turn_on = False
        turn_off = False

        with self.lock:
            if needed:
                if controller in self.rf_power_needed:
                    return  # no change
                else:
                    was_needed = bool(self.rf_power_needed)
                    self.rf_power_needed.add(controller)
                    if not was_needed:
                        # turn on rf power
                        turn_on = True
            else:
                if controller in self.rf_power_needed:
                    self.rf_power_needed.discard(controller)
                    if not self.rf_power_needed:
                        # turn off rf power
                        turn_off = True
                else:
                    return  # no change

        if turn_on:
            self.enable_all_rf_power()
        elif turn_off:
            self.disable_all_rf_power()

    def create_remote(self, controller: DeviceController,
                      serial_number_str: str, subproxy: DeviceSubProxy,
                      parties: set[str]) -> DeviceController:
        reconnect_info = {"type": "remote", "serial_number": serial_number_str}

        parent_sn = controller.serial_number
        serial_numbers = (parent_sn, serial_number_str)

        new_controller = self._update_or_create_controller(
            serial_numbers, None, reconnect_info, controller, parties)

        self._start_proxy(subproxy, new_controller)

        return new_controller

    @QtCore.Slot(object, object)
    def active_triggers_changed_cb(self, controller: DeviceController,
                                   active_triggers: frozenset[str]) -> None:
        with self.lock:
            try:
                last = self.controller_active_triggers[controller]
            except KeyError:
                last = frozenset()

            if last == active_triggers:
                return  # no change

            if not active_triggers:
                try:
                    del self.controller_active_triggers[controller]
                except KeyError:
                    pass
            else:
                self.controller_active_triggers[controller] = active_triggers

            new_active_triggers = frozenset().union(
                *self.controller_active_triggers.values())

            if self.active_triggers != new_active_triggers:
                self.active_triggers = new_active_triggers
                self.active_triggers_changed.emit(new_active_triggers)

                for controller in self.controllers.values():
                    controller.set_global_active_triggers(new_active_triggers)

    def register_old_calc_process(self, calc_process: CalcProcess) -> None:
        self.background_join_deque.append(calc_process.join)

    def register_old_proxy(self, proxy: Proxy) -> None:
        self.background_join_deque.append(proxy.wait_for_close)

    def upload_file(self, filename: str) -> None:
        if self.upload_manager:
            self.upload_manager.upload(filename)

    def get_controller(self, serial_numbers: tuple[str, ...],
                       registration_str: str) -> DeviceController:
        if len(serial_numbers) > 1:
            party = f"parent-{serial_numbers[-1]}"
            parent_controller = self.get_controller(serial_numbers[:-1], party)
        else:
            parent_controller = None
        controller = self._update_or_create_controller(
            serial_numbers, None, None, parent_controller, {registration_str})
        return controller

    def mark_manually_disconnected(self, controller: DeviceController) -> None:
        with self.lock:
            serial_number_tuples: set[tuple[str, ...]] = set()
            for serial_numbers, c in self.controllers.items():
                if c == controller:
                    serial_number_tuples.add(serial_numbers)
            self.manually_disconnected.update(serial_number_tuples)
