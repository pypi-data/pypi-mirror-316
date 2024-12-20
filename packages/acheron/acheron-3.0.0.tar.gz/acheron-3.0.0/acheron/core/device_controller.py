from __future__ import annotations
import datetime
import enum
import functools
import logging
import struct
import threading
from typing import (Any, cast, Collection, Optional, Protocol, TYPE_CHECKING,
                    Union)
import weakref
from weakref import ReferenceType

from diskcache import Cache
from PySide6 import QtCore

from asphodel.device_info import DeviceInfo
from ..device_logging import DeviceLoggerAdapter
from ..device_process.proxy import (DeviceOperation, DeviceProxy, Proxy,
                                    SimpleDeviceOperation)

from .main_schedule import DeviceSchedule
from .preferences import get_device_preferences, Preferences
from ..calc_process.types import CalcSettings, ChannelInformation, Trigger
from ..calc_process.runnner import CalcProcess
from ..device_process.bootloader import already_programmed
from ..device_process.remote_funcs import explode
from ..device_process.schedule import OutputConfig, ScheduleItem
from ..device_process.stream_controller import (
    create_remote, HardwareTestFunction, RFTestParams, start_stream_controller,
    stop_stream_controller, StreamControl, StreamSettings, StreamStatus)

if TYPE_CHECKING:
    from .dispatcher import Dispatcher

logger = logging.getLogger(__name__)


@enum.unique
class DeviceControllerState(enum.Enum):
    DISCONNECTED = enum.auto()  # no proxy or reconnecting
    CONNECTING = enum.auto()  # fetching device info
    STREAMING_STARTING = enum.auto()  # started device streams
    RUNNING = enum.auto()  # streaming, packets recieved
    RUNNING_FUNCTION = enum.auto()  # running a dedicated function


@enum.unique
class RFPowerStatus(enum.Enum):
    NOT_SUPPORTED = enum.auto(
    )  # device disconnected or does not support RF power
    DISABLED = enum.auto()  # rf power supported but disabled
    ENABLED = enum.auto()  # rf power enabled


MANUAL_CONTROL = "manual"
REMOTE_CONTROL = "remote"


class HardwareTestCallback(Protocol):
    def hardware_test_function_finished(self, test_id: str, data: Any) -> None:
        ...

    def hardware_test_run_finished(self) -> None:
        ...


class DeviceController(QtCore.QObject):
    state_changed_signal = QtCore.Signal(object, str)
    disconnected_signal = QtCore.Signal(object)  # self
    progress_signal = QtCore.Signal(int, int, str)

    rgb_updated = QtCore.Signal(int, object)
    led_updated = QtCore.Signal(int, int)
    ctrl_var_updated = QtCore.Signal(int, int)

    rf_power_changed = QtCore.Signal(object, object)  # self, RFPowerStatus
    rf_power_needed = QtCore.Signal(object, bool)  # self, needed

    # self, frozenset[str], frozenset[str]
    active_triggers_changed = QtCore.Signal(object, object, object)
    alerts_changed = QtCore.Signal(object)  # frozenset[str]

    scan_data = QtCore.Signal(object, object)  # self, list[ScanResult]

    # self, serial, active_scan
    active_scan_data = QtCore.Signal(object, int, object)

    # self, serial, bootloader
    remote_connecting = QtCore.Signal(object, int, bool)

    scan_first_pass = QtCore.Signal()

    manual_control_changed = QtCore.Signal(bool)

    ongoing_items = QtCore.Signal(object)  # set[str]

    trigger_count_changed = QtCore.Signal(int)
    schedule_count_changed = QtCore.Signal(int)

    rf_test_finished = QtCore.Signal()

    # serial | None, bootloader, streaming
    remote_target_changed = QtCore.Signal(object, bool, bool)

    remote_connected = QtCore.Signal(bool)
    remote_target_connected = QtCore.Signal(bool)

    # NOTE: the rest of these are emitted directly from calc_process

    # channel_id, mean, std
    channel_update = QtCore.Signal(object, object, object)

    # channel_id, time_array, data_array
    plot_update = QtCore.Signal(object, object, object)

    # channel_id, subchannel_id, fft_freqs, fft_data
    # NOTE: data may be a scalar from 0 to 1 showing buffering status
    fft_update = QtCore.Signal(object, object, object, object)

    # total, last_datetime, recent
    lost_packet_update = QtCore.Signal(object, object, object)

    def __init__(self, dispatcher: "Dispatcher",
                 serial_number: str,
                 preferences: Preferences,
                 diskcache: Cache,
                 schedule: DeviceSchedule,
                 calc_process_name: str,
                 disable_streaming: bool,
                 disable_archiving: bool,
                 parent_controller: Optional["DeviceController"],
                 parties: set[str]) -> None:
        super().__init__()

        self.dispatcher = dispatcher
        self.serial_number = serial_number
        self.preferences = preferences
        self.diskcache = diskcache
        self.schedule = schedule
        self.calc_process_name = calc_process_name
        self.disable_streaming = disable_streaming
        self.disable_archiving = disable_archiving
        self.parent_controller = parent_controller
        self.parties = parties.copy()
        if not self.parties:
            self.parties.add(MANUAL_CONTROL)

        # initialize
        self.display_name = serial_number

        self.device_prefs = get_device_preferences(serial_number)

        self.state: DeviceControllerState = DeviceControllerState.DISCONNECTED
        self.proxy: Optional[Proxy] = None
        self.proxy_finished = threading.Event()
        self.proxy_finished.set()
        self.device_info: Optional[DeviceInfo] = None

        # create a logger that includes the serial number information
        self.logger = DeviceLoggerAdapter(logger, self.serial_number)

        self.is_shown = False

        self.channel_info: dict[int, ChannelInformation] = {}
        self.active_streams: frozenset[int] = frozenset()
        self.desired_streams: Optional[frozenset[int]] = None

        self.streaming = False
        self.calc_process: Optional[CalcProcess] = None
        self.stream_settings: Optional[StreamSettings] = None
        self.calc_settings: Optional[CalcSettings] = None

        self.remote_target_serial: Optional[int] = None
        self.remote_target_controller: Optional[DeviceController] = None
        self.remote_target_bootloader = False
        self.remote_target_streaming = True
        self.default_remote_target: Optional[int] = None
        self.remote_controller: Optional[DeviceController] = None  # active

        self.hardware_test_callbacks: dict[str, HardwareTestCallback] = {}
        self.hardware_run_id = 0

        self.registered_triggers: dict[str, set[Trigger]] = {}
        self.alert_triggers: dict[str, Trigger] = {}
        self.trigger_count: int = 0

        self.last_emitted_active_triggers: frozenset[str] = frozenset()
        self.trigger_names: frozenset[str] = frozenset()  # no alerts

        self.schedule_count: int = 0
        self.main_schedule_id = f"_main_{self.serial_number}"

        self.schedule.deleted_items.connect(self.schedule_items_deleted)
        self.schedule.updated_item.connect(self.schedule_item_updated)

        self._setup_proxy_operations()

    def _setup_proxy_operations(self) -> None:
        self.start_stream_controller_op = DeviceOperation(
            start_stream_controller)

        self.stop_stream_controller_op = DeviceOperation(
            stop_stream_controller)
        self.stop_stream_controller_op.completed.connect(
            self._stop_stream_controller_cb)

        self.close_device_op = SimpleDeviceOperation("close")

    def update_preferences(self) -> None:
        if self.calc_process is None:
            return

        if self.calc_settings is None or self.stream_settings is None:
            # not streaming
            return

        stream_settings, calc_settings = self._get_settings()

        if self.calc_settings != calc_settings:
            self.calc_settings = calc_settings
            self.calc_process.change_settings(calc_settings)

        if self.stream_settings != stream_settings:
            self.stream_settings = stream_settings
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.CHANGE_SETTINGS, stream_settings))

        self._update_alert_triggers()

    def update_disable_streaming(self, disable: bool) -> None:
        self.disable_streaming = disable

        self._update_main_schedule_item()

    def update_disable_archiving(self, disable: bool) -> None:
        if disable:
            self.logger.info("Disabling archiving")
        else:
            self.logger.info("Enabling archiving")

        self.disable_archiving = disable

        self._update_main_schedule_item()

    def set_active_streams(self, streams: Optional[Collection[int]]) -> None:
        # override the global streaming disable
        self.disable_streaming = False

        if streams is None:
            self.desired_streams = None
        else:
            self.desired_streams = frozenset(streams)

        self._update_main_schedule_item()

    def _set_state(self, state: DeviceControllerState, message: str) -> None:
        if self.state == state:
            return

        self.state = state
        self.state_changed_signal.emit(state, message)

        if state == DeviceControllerState.DISCONNECTED:
            self.logger.info("Disconnected")
            self.disconnected_signal.emit(self)

    def set_proxy(self, proxy: Proxy) -> None:
        if self.proxy:
            self._error(self.tr("Reconnecting"))

        self.proxy = proxy
        self.proxy_finished.clear()
        self.proxy.disconnected.connect(
            functools.partial(self._proxy_disconnect_cb, weakref.ref(proxy)))

        self._start_stream_controller()  # calls _set_state

    def _proxy_disconnect_cb(self, proxy_ref: "ReferenceType[Proxy]") -> None:
        proxy = proxy_ref()
        if proxy is None:
            return

        # proxy is dead at this point, no way to update LEDs or stop streaming

        if self.proxy == proxy:
            self.proxy = None
            self.proxy_finished.set()
            self._error(self.tr("Device Disconnected"))

        self.dispatcher.register_old_proxy(proxy)

    def _streaming_disconnected(self, message: str) -> None:
        self.dispatcher.connectivity_manager.stop_device(self.serial_number)
        self.active_triggers_changed.emit(
            self, frozenset(), self.trigger_names)
        self.last_emitted_active_triggers = frozenset()
        self._set_state(DeviceControllerState.DISCONNECTED, message)

        self._stop_rf_power_handling()
        self.rf_power_needed.emit(self, False)
        self._set_schedule_count(0)

    def _error(self, message: str) -> None:
        if self.streaming:
            self.streaming = False
            if self.calc_process:
                # start stopping calc process now
                self.calc_process.stop()
                if not self.proxy:
                    self.calc_process.close()
                    self.dispatcher.register_old_calc_process(
                        self.calc_process)
                    self.calc_process = None
            if self.proxy:
                # NOTE: the callback for this will close the calc process
                self.proxy.send_job(self.stop_stream_controller_op)
        self._disconnect_proxy()

        self._streaming_disconnected(message)

        self._remote_disconnected_cb()

    def _disconnect_proxy(self) -> None:
        if self.proxy:
            self.proxy.send_job(self.close_device_op)
            self.proxy.close_connection()
            self.dispatcher.register_old_proxy(self.proxy)
            self.proxy = None
            self.proxy_finished.set()

    @QtCore.Slot()
    def _stop_stream_controller_cb(self) -> None:
        if self.calc_process:
            self.calc_process.close()
            self.dispatcher.register_old_calc_process(self.calc_process)
            self.calc_process = None

    def stop(self) -> None:
        self._error(self.tr("Closed"))

    def join(self) -> None:
        self.proxy_finished.wait()

    def _get_settings(self) -> tuple[StreamSettings, CalcSettings]:
        interval = datetime.timedelta(
            minutes=self.preferences.archive_interval)
        output_config = OutputConfig(
            compression_level=self.preferences.compression_level,
            base_name=None,
            base_directory=self.preferences.base_dir,
            device_directory=True,
            date_dir_structure=True,
            datetime_filename=True,
            roll_over_interval=interval,
            upload_marker=self.preferences.upload_enabled,
        )

        stream_settings = StreamSettings(
            auto_rgb=self.preferences.auto_rgb,
            response_time=self.device_prefs.response_time,
            buffer_time=self.device_prefs.buffer_time,
            timeout=self.device_prefs.stream_timeout,
            default_output_config=output_config
        )

        calc_settings = CalcSettings(
            channel_interval=self.preferences.update_timer_interval / 1000,
            plot_interval=self.preferences.graph_timer_interval / 1000,
            fft_interval=self.preferences.graph_timer_interval / 1000,
            downsample=self.preferences.downsample,
        )

        return (stream_settings, calc_settings)

    def _update_main_schedule_item(self) -> None:
        schedule_item: Optional[ScheduleItem]

        if MANUAL_CONTROL not in self.parties:
            self.schedule.clear_partition(self.main_schedule_id)
        else:
            active_streams: Optional[frozenset[int]]

            if self.disable_streaming:
                active_streams = frozenset()
            else:
                active_streams = self.desired_streams

            schedule_item = ScheduleItem(
                id=self.main_schedule_id,
                active_streams=active_streams,
                start_time=None,  # asap
                collection_time=None,
                stop_time=None,
                duration=None,
                failure_time=None,
                output_config=None if self.disable_archiving else True,
            )
            # NOTE: using the schedule id as the partition name
            self.schedule.add_item(self.main_schedule_id, schedule_item)

    def _update_remote_schedule_item(self) -> None:
        if self.remote_target_serial and MANUAL_CONTROL in self.parties:
            schedule_item = ScheduleItem(
                id="_remote",
                remote_sn=self.remote_target_serial,
                remote_bootloader=self.remote_target_bootloader,
                start_time=None,  # asap
                collection_time=None,
                stop_time=None,
                duration=None,
                failure_time=None,
                output_config=None,
            )
            # NOTE: using the schedule id as the partition name
            self.schedule.add_item("_remote", schedule_item)
        else:
            self.schedule.clear_partition("_remote")

    def _update_schedule_items(self) -> None:
        self._update_main_schedule_item()
        self._update_remote_schedule_item()

    def _start_stream_controller(self) -> None:
        self.device_info = None
        if not self.proxy:
            return

        self.streaming = True

        self._set_state(DeviceControllerState.CONNECTING,
                        self.tr("Loading device information..."))

        self.stream_settings, self.calc_settings = self._get_settings()

        if self.calc_process:
            self.calc_process.stop()
            self.dispatcher.register_old_calc_process(self.calc_process)
            self.calc_process = None

        self._update_schedule_items()
        schedule_items = self.schedule.get_items()

        self._update_alert_triggers()
        self.triggers = self._get_triggers()

        self.calc_process = CalcProcess(
            self.calc_process_name, self.serial_number, self.is_shown,
            self.calc_settings, self.triggers)

        self.proxy.disconnected.connect(self.calc_process.close)

        self.calc_process.processing_start.connect(self._processing_start_cb)
        self.calc_process.processing_stop.connect(self._processing_stop_cb)
        self.calc_process.status_received.connect(self._status_cb)
        self.calc_process.channel_update.connect(self.channel_update)
        self.calc_process.plot_update.connect(self.plot_update)
        self.calc_process.fft_update.connect(self.fft_update)
        self.calc_process.lost_packet_update.connect(self.lost_packet_update)
        self.calc_process.unknown_id.connect(self._unknown_id_cb)
        self.calc_process.active_triggers_changed.connect(
            self._active_triggers_changed_cb)
        ctrl_pipe, packet_pipe, status_pipe = self.calc_process.get_pipes()

        self.proxy.send_job(
            self.start_stream_controller_op, self.stream_settings,
            schedule_items, self.main_schedule_id,
            self.dispatcher.active_triggers, self.diskcache, ctrl_pipe,
            packet_pipe, status_pipe)

    @QtCore.Slot()
    def do_explode(self) -> None:
        if self.proxy:
            self.proxy.send_job(DeviceOperation(explode))

    @QtCore.Slot()
    def force_run_bootloader(self) -> None:
        if self.calc_process:
            message = self.tr("Connecting to bootloader...")
            self.logger.info(message)
            self._set_state(DeviceControllerState.CONNECTING, message)
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.FORCE_RUN_BOOTLOADER,))

    @QtCore.Slot()
    def force_run_application(self) -> None:
        if self.calc_process:
            message = self.tr("Connecting to application...")
            self.logger.info(message)
            self._set_state(DeviceControllerState.CONNECTING, message)
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.FORCE_RUN_APPLICATION,))

    @QtCore.Slot()
    def force_reset(self) -> None:
        if self.calc_process:
            message = self.tr("Resetting device...")
            self.logger.info(message)
            self._set_state(DeviceControllerState.CONNECTING, message)
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.FORCE_RESET,))

    def write_nvm(self, nvm: Union[bytes, bytearray]) -> None:
        if self.calc_process is None or self.device_info is None:
            self.logger.warning("Connot write NVM while disconnected!")
            return

        nvm = bytes(nvm)
        if self.device_info.nvm != nvm:
            self.device_info.nvm = nvm  # this may not be necessary
            message = self.tr("Writing NVM...")
            self._set_state(DeviceControllerState.CONNECTING, message)
            self.logger.info(message)
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.WRITE_NVM, nvm))
        elif self.device_info.nvm_modified is True:
            self.force_reset()
        else:
            self.logger.info("No change to NVM. Skipping write.")
            return

    @QtCore.Slot(object)
    def _unknown_id_cb(self, unknown_id: int) -> None:
        msg = "Unknown ID {} while decoding packet".format(unknown_id)
        self.logger.error(msg)

    def set_global_active_triggers(self,
                                   active_triggers: frozenset[str]) -> None:
        if self.calc_process:
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.ACTIVE_TRIGGERS_CHANGED, active_triggers))

    def _get_triggers(self) -> set[Trigger]:
        old_triggers_count = self.trigger_count
        all_triggers: set[Trigger] = set()
        all_triggers.update(*self.registered_triggers.values())
        self.trigger_count = len(all_triggers)
        if old_triggers_count != self.trigger_count:
            self.trigger_count_changed.emit(self.trigger_count)
        return all_triggers

    def _update_trigger_names(self) -> None:
        trigger_names: set[str] = set()
        for key, triggers in self.registered_triggers.items():
            if key != "alerts":
                trigger_names.update(t.id for t in triggers)
        new_trigger_names = frozenset(trigger_names)
        if new_trigger_names != self.trigger_names:
            inactive = new_trigger_names.difference(
                self.last_emitted_active_triggers)
            self.active_triggers_changed.emit(
                self, self.last_emitted_active_triggers, inactive)
            self.trigger_names = new_trigger_names

    def register_triggers(self, key: str, triggers: set[Trigger]) -> None:
        old_triggers = self.registered_triggers.get(key)
        if old_triggers == triggers:
            # nothing new
            return

        self.registered_triggers[key] = triggers

        self._update_trigger_names()

        if self.calc_process:
            triggers = self._get_triggers()
            if self.triggers != triggers:
                self.triggers = triggers
                self.calc_process.change_triggers(triggers)

    def _update_alert_triggers(self) -> None:
        triggers: set[Trigger] = set()
        alert_triggers: dict[str, Trigger] = {}

        alert_limits = self.device_prefs.get_all_alert_limits()
        for limit_type, channel_id, subchannel_index, value in alert_limits:
            id = f'_alert_{channel_id}_{subchannel_index}_{limit_type}'
            trigger = Trigger(
                id=id,
                channel_id=channel_id,
                subchannel_index=subchannel_index,
                limit_type=limit_type,
                activate_limit=value,
                deactivate_limit=value,
            )
            triggers.add(trigger)
            alert_triggers[id] = trigger

        self.alert_triggers = alert_triggers

        self.register_triggers("alerts", triggers)

    def _email_callback(self, exception: Optional[Exception]) -> None:
        # NOTE: this may be called in a different thread!
        if exception is None:
            self.logger.info("Sent alert email")
        else:
            self.logger.error("Error sending alert email", exc_info=exception)

    @QtCore.Slot(object)
    def _active_triggers_changed_cb(self, active_triggers: set[str]) -> None:
        alerts = frozenset(t for t in active_triggers
                           if t.startswith("_alert"))
        without_alerts = frozenset(t for t in active_triggers
                                   if not t.startswith("_alert"))
        if without_alerts != self.last_emitted_active_triggers:
            triggers_on = without_alerts.difference(
                self.last_emitted_active_triggers)
            triggers_off = self.last_emitted_active_triggers.difference(
                without_alerts)
            for trigger_name in sorted(triggers_on):
                self.logger.info("Trigger enabled: %s", trigger_name)
            for trigger_name in sorted(triggers_off):
                self.logger.info("Trigger disabled: %s", trigger_name)
            inactive = self.trigger_names.difference(without_alerts)
            self.active_triggers_changed.emit(self, without_alerts, inactive)
            self.last_emitted_active_triggers = without_alerts
        self.alerts_changed.emit(alerts)

        # find triggers and subchannel names
        trigger_list: list[tuple[Trigger, str]] = []
        for alert in alerts:
            trigger = self.alert_triggers.get(alert)
            if not trigger:
                continue
            channel_info = self.channel_info.get(trigger.channel_id)
            if not channel_info:
                continue
            try:
                subchannel_name = channel_info.subchannel_names[
                    trigger.subchannel_index]
                trigger_list.append((trigger, subchannel_name))
            except IndexError:
                continue

        if trigger_list:
            self.dispatcher.alert_manager.send_alerts(
                self.logger, self.serial_number, self.display_name,
                trigger_list, self._email_callback)

    @QtCore.Slot(object, object, object)
    def _processing_start_cb(
            self, device_info: DeviceInfo, active_streams: frozenset[int],
            channel_info: dict[int, ChannelInformation]) -> None:
        self.device_info = device_info
        self.channel_info = channel_info
        self.active_streams = active_streams

        # pull out display name
        if device_info.user_tag_1:
            self.display_name = device_info.user_tag_1
        else:
            self.display_name = self.serial_number

        self._set_state(DeviceControllerState.STREAMING_STARTING,
                        self.tr("Starting streaming..."))
        connected_message = self.tr("Connected")
        self._set_state(DeviceControllerState.RUNNING, connected_message)
        self.logger.info(connected_message)

        self.start_connectivity()

        rf_power_status = self._start_rf_power_handling()

        if rf_power_status == RFPowerStatus.ENABLED:
            self.logger.info("RF power already running")

        if device_info.supports_radio:
            if device_info.radio_default_serial:
                self.default_remote_target = device_info.radio_default_serial
                if self.remote_target_serial is None:
                    self.set_remote_target(
                        device_info.radio_default_serial, False)
            else:
                self.default_remote_target = None
        else:
            self.default_remote_target = None
            self.clear_remote_target()

        # because we're using device_info from the calc process instead of the
        # one provided in the _status_cb(), the RGB states are usually out of
        # date. We need to just ask for an update so everything gets synced up
        if self.calc_process:
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.GET_RGB_STATE,))

    @QtCore.Slot()
    def _processing_stop_cb(self) -> None:
        self.device_info = None
        self.channel_info.clear()
        self.active_streams = frozenset()

        message = self.tr("Device Stopped")
        self.logger.debug(message)
        self._streaming_disconnected(message)

    @QtCore.Slot(object)
    def _status_cb(self, status: tuple[Any, ...]) -> None:
        status_type = status[0]
        if status_type == StreamStatus.RECONNECTING:
            self._set_state(DeviceControllerState.CONNECTING,
                            self.tr("Reconnecting..."))
        elif status_type == StreamStatus.DEVICE_INFO_START:
            self._set_state(DeviceControllerState.CONNECTING,
                            self.tr("Loading device information..."))
        elif status_type == StreamStatus.DEVICE_INFO_PROGRESS:
            finished, total, _section_name = status[1:]
            message = self.tr("Loading device information...")
            self.progress_signal.emit(finished, total, message)
        elif status_type == StreamStatus.WRITE_NVM_PROGRESS:
            # finished, total = status[1:]
            pass  # ignore this, at least for now
        elif status_type == StreamStatus.DEVICE_INFO_READY:
            pass  # nothing to do here, wait for info through the calc process
        elif status_type == StreamStatus.STREAMING_STARTED:
            pass  # nothing to do here, wait for info through the calc process
        elif status_type == StreamStatus.STREAMING_ERROR_TIMEOUT:
            self.logger.warning("Stream Timeout")
        elif status_type == StreamStatus.STREAMING_ERROR_DISCONNECT:
            self.logger.warning("Stream Disconnect")
        elif status_type == StreamStatus.STREAMING_ERROR_OTHER:
            # err_id = status[1]
            self.logger.warning("Stream Error")
            self._error(self.tr("Stream Error"))
        elif status_type == StreamStatus.BOOTLOADER_PROGRESS:
            finished, total, status_str = status[1:]
            self.progress_signal.emit(finished, total, status_str)
        elif status_type == StreamStatus.BOOTLOADER_FINISHED:
            success, event_data = status[1:]
            self.dispatcher.event_uploader.firmware_updated(
                self.serial_number, success, event_data)
        elif status_type == StreamStatus.DISCONNECTED:
            self._error(self.tr("Disconnected"))
        elif status_type == StreamStatus.RGB_UPDATE:
            index, values = status[1:]
            if self.device_info and len(self.device_info.rgb_settings) > index:
                self.device_info.rgb_settings[index] = values
                self.rgb_updated.emit(index, values)
        elif status_type == StreamStatus.DEVICE_MODE_UPDATE:
            success, mode = status[1:]
            if success:
                if self.device_info:
                    self.device_info.device_mode = mode
            else:
                self.logger.error("Bad device mode {}".format(mode))
        elif status_type == StreamStatus.STARTED_FILE:
            file_path, schedule_id, marked_for_upload = status[1:]
            self.logger.debug("Starting file %s", file_path)
        elif status_type == StreamStatus.FINISHED_FILE:
            file_path, schedule_id, marked_for_upload = status[1:]
            self.logger.debug("Finished file %s", file_path)
            if marked_for_upload:
                self.dispatcher.upload_file(file_path)
        elif status_type == StreamStatus.ONGOING_ITEMS:
            schedule_ids_set = status[1]
            rf_power_needed = status[2]
            schedule_count = status[3]
            self.rf_power_needed.emit(self, rf_power_needed)
            self.ongoing_items.emit(schedule_ids_set)
            self._set_schedule_count(schedule_count)
        elif status_type == StreamStatus.FINISHED_ITEM:
            schedule_id, success = status[1:]
            self.schedule.mark_finished(schedule_id, success)
        elif status_type == StreamStatus.HARDWARE_TEST_FUNCTION_FINISHED:
            run_id = status[1]
            test_id = status[2]
            data = status[3]
            try:
                callback = self.hardware_test_callbacks[run_id]
                callback.hardware_test_function_finished(test_id, data)
            except KeyError:
                self.logger.error(
                    "Missing handware test finished callback for %s", run_id)
        elif status_type == StreamStatus.HARDWARE_TEST_RUN_FINISHED:
            run_id = status[1]
            try:
                callback = self.hardware_test_callbacks.pop(run_id)
                callback.hardware_test_run_finished()
            except KeyError:
                self.logger.error(
                    "Missing handware run finished callback for %s", run_id)
        elif status_type == StreamStatus.RF_TEST_FINISHED:
            self.rf_test_finished.emit()
        elif status_type == StreamStatus.REMOTE_CONNECTING:
            serial_number_int = status[1]
            bootloader = status[2]
            self.remote_connecting.emit(self, serial_number_int, bootloader)
        elif status_type == StreamStatus.REMOTE_CONNECTED:
            self._remote_connected_cb(*status[1:])
        elif status_type == StreamStatus.REMOTE_DISCONNECTED:
            self._remote_disconnected_cb()
        elif status_type == StreamStatus.SCAN_DATA:
            scans = status[1]
            self.scan_data.emit(self, scans)
        elif status_type == StreamStatus.ACTIVE_SCAN_DATA:
            serial, active_scan = status[1:]
            self.active_scan_data.emit(self, serial, active_scan)
        elif status_type == StreamStatus.SCAN_FIRST_PASS:
            self.scan_first_pass.emit()
        elif status_type == StreamStatus.RADIO_FUNCTION_FINISHED:
            self.logger.info("Unhandled: %s", status)  # TODO: implement

    def set_user_tag(self, index: int, s: str) -> None:
        if self.device_info is None:
            raise AssertionError("No device information")

        tag_key = "user_tag_" + str(index + 1)

        # find the offset and length
        offset, length = self.device_info.tag_locations[index]

        setattr(self.device_info, tag_key, s)
        b = s.encode("UTF-8")
        new_nvm = bytearray(self.device_info.nvm)
        struct.pack_into("{}s".format(length), new_nvm, offset, b)

        # write the new tag
        self.write_nvm(new_nvm)

    def set_is_shown(self, is_shown: bool) -> None:
        self.is_shown = is_shown
        if self.calc_process:
            self.calc_process.set_is_shown(is_shown)

    def plot_change(self, channel_id: Optional[int],
                    subchannel_index: Optional[int]) -> None:
        if self.calc_process:
            self.calc_process.plot_change(channel_id, subchannel_index)

    def reset_lost_packets(self) -> None:
        if self.calc_process:
            self.calc_process.reset_lost_packets()

    def set_device_mode(self, new_mode: int) -> None:
        if self.calc_process is not None and self.device_info:
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.SET_DEVICE_MODE, new_mode))

    def set_rgb(self, index: int, values: tuple[int, int, int]) -> None:
        if self.calc_process is not None and self.device_info:
            try:
                if self.device_info.rgb_settings[index] == values:
                    return
                self.device_info.rgb_settings[index] = values
            except IndexError:
                return
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.SET_RGB, index, values))
            self.rgb_updated.emit(index, values)

    def set_led(self, index: int, value: int) -> None:
        if self.calc_process is not None and self.device_info:
            try:
                if self.device_info.led_settings[index] == value:
                    return
                self.device_info.led_settings[index] = value
            except IndexError:
                return
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.SET_LED, index, value))
            self.led_updated.emit(index, value)

    def set_ctrl_var(self, index: int, value: int) -> None:
        if self.calc_process is not None and self.device_info:
            try:
                old = self.device_info.ctrl_vars[index]
            except IndexError:
                return
            if old[2] == value:
                return
            self.device_info.ctrl_vars[index] = (old[0], old[1], value)
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.SET_CTRL_VAR, index, value))
            self.ctrl_var_updated.emit(index, value)

    def _start_rf_power_handling(self) -> RFPowerStatus:
        status = self.get_rf_power_status()
        self.rf_power_changed.emit(self, status)
        return status

    def _stop_rf_power_handling(self) -> None:
        # this controller is no longer handling rf power
        self.rf_power_changed.emit(self, RFPowerStatus.NOT_SUPPORTED)

    def get_rf_power_status(self) -> RFPowerStatus:
        if not self.device_info or self.device_info.rf_power_status is None:
            return RFPowerStatus.NOT_SUPPORTED

        if self.device_info.rf_power_status:
            return RFPowerStatus.ENABLED
        else:
            return RFPowerStatus.DISABLED

    @QtCore.Slot()
    def enable_rf_power(self) -> None:
        if self.calc_process is not None and self.device_info:
            if self.device_info.supports_rf_power:
                self.device_info.rf_power_status = True
                self.logger.info("Enabling RF power")
                self.calc_process.send_stream_ctrl_message(
                    (StreamControl.SET_RF_POWER, True))
                self.rf_power_changed.emit(self, RFPowerStatus.ENABLED)

    @QtCore.Slot()
    def disable_rf_power(self) -> None:
        if self.calc_process is not None and self.device_info:
            if self.device_info.supports_rf_power:
                self.device_info.rf_power_status = False
                self.logger.info("Disabling RF power")
                self.calc_process.send_stream_ctrl_message(
                    (StreamControl.SET_RF_POWER, False))
                self.rf_power_changed.emit(self, RFPowerStatus.DISABLED)

    def load_firmware(self, firmware_data: dict[str, Any], url: str) -> None:
        if self.calc_process is None or not self.device_info:
            return

        if already_programmed(firmware_data, self.device_info):
            self.logger.info("Firmware already present!")
            return

        device_name, device_rev = self.device_info.board_info

        found = False
        board_strs = []
        for rev, name in firmware_data['board']:
            if rev == device_rev and name == device_name:
                found = True
                break
            board_strs.append(f"{name} rev {rev}")

        if not found:
            self.logger.error("Firmware only supports %s!",
                              ", ".join(board_strs))
            return

        if firmware_data['chip'] != self.device_info.chip_model:
            self.logger.error("Firmware only supports chip %s!",
                              firmware_data['chip'])
            return

        # add the url for the event data upload
        firmware_data = firmware_data.copy()
        firmware_data['source'] = url

        message = self.tr("Loading firmware...")
        self._set_state(DeviceControllerState.CONNECTING, message)
        self.calc_process.send_stream_ctrl_message(
                (StreamControl.DO_BOOTLOADER, firmware_data))

    def start_active_scan(self, serial_number: int, bootloader: bool) -> None:
        if self.calc_process is None:
            self.active_scan_data.emit(self, serial_number, None)
        else:
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.DO_ACTIVE_SCAN, serial_number, bootloader))

    def set_remote_target(self, serial_number: int, bootloader: bool,
                          streaming: bool = True) -> None:
        self.remote_target_serial = serial_number
        self.remote_target_bootloader = bootloader
        self.remote_target_streaming = streaming

        if self.remote_target_controller:
            self.remote_target_controller.manual_control_changed.disconnect(
                self._remote_target_manual_control_changed_cb)
            self.remote_target_controller.release_party(MANUAL_CONTROL)
            self.remote_target_connected.emit(False)
            self.remote_target_controller = None
        self._update_remote_schedule_item()
        self.remote_target_changed.emit(serial_number, bootloader, streaming)

    def clear_remote_target(self) -> None:
        self.remote_target_serial = None
        if self.remote_target_controller:
            self.remote_target_controller.manual_control_changed.disconnect(
                self._remote_target_manual_control_changed_cb)
            self.remote_target_controller.release_party(MANUAL_CONTROL)
            self.remote_target_connected.emit(False)
            self.remote_target_controller = None
        self._update_remote_schedule_item()
        self.remote_target_changed.emit(None, False, False)

    def _remote_connected_cb(self, serial_number_int: int,
                             serial_number_str: str, bootloader: bool) -> None:
        if not self.proxy:
            return

        subproxy = cast(DeviceProxy, self.proxy).create_subproxy(
            create_remote, serial_number_int, bootloader)

        parties = {REMOTE_CONTROL}

        if self.remote_target_serial == serial_number_int:
            parties.add(MANUAL_CONTROL)

        self.remote_controller = self.dispatcher.create_remote(
            self, serial_number_str, subproxy, parties)

        self.remote_connected.emit(True)

        if self.remote_target_serial == serial_number_int:
            self.remote_target_controller = self.remote_controller
            self.remote_target_controller.manual_control_changed.connect(
                self._remote_target_manual_control_changed_cb)
            self.remote_target_connected.emit(True)

            if not self.remote_target_streaming:
                self.remote_target_controller.set_active_streams(frozenset())
        elif self.remote_target_controller:
            self.remote_target_controller.release_party(REMOTE_CONTROL)
            self.remote_target_controller.manual_control_changed.disconnect(
                self._remote_target_manual_control_changed_cb)
            self.remote_target_connected.emit(False)
            self.remote_target_controller = None

    def _remote_disconnected_cb(self) -> None:
        if self.remote_controller:
            self.remote_controller.release_party(REMOTE_CONTROL)
            self.remote_connected.emit(False)
            self.remote_controller = None
        self.remote_target_connected.emit(False)

    @QtCore.Slot(bool)
    def _remote_target_manual_control_changed_cb(self,
                                                 manual_control: bool) -> None:
        if not manual_control:
            self.clear_remote_target()

    def run_hardware_tests(
            self, functions: list[tuple[HardwareTestFunction, str]],
            callback: HardwareTestCallback) -> None:
        run_id = str(self.hardware_run_id)
        self.hardware_run_id += 1
        self.hardware_test_callbacks[run_id] = callback

        if self.calc_process is not None:
            self.calc_process.send_stream_ctrl_message(
                    (StreamControl.DO_HARDWARE_TESTS, functions, run_id))

    def register_parties(self, parties: set[str]) -> None:
        was_manually_controlled = MANUAL_CONTROL in self.parties
        self.parties.update(parties)
        if MANUAL_CONTROL in parties and not was_manually_controlled:
            self._update_schedule_items()
            self.manual_control_changed.emit(True)

    def release_party(self, party: str) -> None:
        if party not in self.parties:
            return  # no change

        was_manually_controlled = MANUAL_CONTROL in self.parties
        self.parties.discard(party)
        if self.parties:
            if party == MANUAL_CONTROL and was_manually_controlled:
                self._update_schedule_items()
                self.manual_control_changed.emit(False)
        else:
            # time to stop controller
            self.dispatcher.stop_controller(self)

    def clear_manual_control(self) -> None:
        self.release_party(MANUAL_CONTROL)

    def get_manual_control(self) -> bool:
        return MANUAL_CONTROL in self.parties

    def _set_schedule_count(self, schedule_count: int) -> None:
        if schedule_count != self.schedule_count:
            self.schedule_count = schedule_count
            self.schedule_count_changed.emit(schedule_count)

    def start_connectivity(self) -> None:
        if self.calc_process is not None and self.channel_info:
            pipe = self.dispatcher.connectivity_manager.create_device_pipe(
                self.serial_number, self.channel_info)
            if pipe is not None:
                self.calc_process.set_connectivity_pipe(pipe)

    def start_rf_test(self, params: RFTestParams) -> None:
        if self.calc_process is not None:
            self.calc_process.send_stream_ctrl_message(
                    (StreamControl.DO_RF_TEST, params))
        else:
            raise RuntimeError("Not connected")

    @QtCore.Slot(object)
    def schedule_items_deleted(self, ids: set[str]) -> None:
        if self.calc_process:
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.DELETE_SCHEDULE_IDS, ids))

    @QtCore.Slot(object)
    def schedule_item_updated(self, schedule_item: ScheduleItem) -> None:
        if self.calc_process:
            self.calc_process.send_stream_ctrl_message(
                (StreamControl.UPDATE_SCHEDULE_ITEM, schedule_item))
