import logging
import re
import struct
import threading
from typing import Any, cast, Iterable, Optional

from intervaltree import Interval, IntervalTree
import numpy
from numpy.typing import NDArray
from pymodbus.server.sync import ModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusServerContext
from pymodbus.interfaces import IModbusSlaveContext
from pymodbus.transaction import ModbusSocketFramer
from PySide6 import QtCore

from asphodel import AsphodelChannelInfo

from hyperborea.ringbuffer import RingBuffer

from .connectivity_manager import DeviceCallback
from ..calc_process.types import ChannelInformation
from ..core.preferences import get_device_preferences, Preferences
from ..device_logging import DeviceLoggerAdapter

logger = logging.getLogger(__name__)


def get_numeric_serial(serial_number: str) -> int:
    matches = re.findall(r'\d+', serial_number)
    return int(matches[-1]) if matches else 0


class ModbusDeviceMapping:
    def __init__(self, serial_number: str,
                 channel_info: dict[int, ChannelInformation]):
        self.serial_number = serial_number
        self.channel_info = channel_info
        self.logger = DeviceLoggerAdapter(logger, serial_number)

        self.mean_ringbuffers: dict[int, RingBuffer] = {}  # by channel_id
        self.instant_ringbuffers: list[RingBuffer] = []  # by modbus index
        self.last_instant_value: list[float] = []  # by modbus index
        self.channel_modbus_index: dict[int, int] = {}  # by channel_id
        self.modbus_index_channel: dict[int, tuple[int, int]] = {}

        for channel_id, info in sorted(channel_info.items()):
            subchannel_count = len(info.subchannel_names)

            self.mean_ringbuffers[channel_id] = RingBuffer(
                info.mean_len, subchannel_count)

            modbus_index = len(self.instant_ringbuffers)
            self.channel_modbus_index[channel_id] = modbus_index

            for i in range(subchannel_count):
                self.instant_ringbuffers.append(RingBuffer(info.mean_len, 1))
                self.last_instant_value.append(0.0)
                self.modbus_index_channel[modbus_index + i] = (channel_id, i)

        # for use externally
        self.channel_count = len(self.instant_ringbuffers)
        self.numeric_serial = get_numeric_serial(serial_number)

    def callback(self, channel_id: int, data: NDArray[numpy.float64]) -> None:
        self.mean_ringbuffers[channel_id].extend(data)

        modbus_index = self.channel_modbus_index[channel_id]
        for i, subchannel_data in enumerate(data.T):
            self.instant_ringbuffers[modbus_index + i].extend(
                subchannel_data[:, None])

    def _mean_to_16bit(self, value: float,
                       channel: AsphodelChannelInfo) -> int:
        try:
            if value >= channel.maximum:
                return 0xFFFF
            elif value <= channel.minimum:
                return 0
            else:
                ratio = ((value - channel.minimum) /
                         (channel.maximum - channel.minimum))
                return round(0xFFFF * ratio)
        except ValueError:
            return 0

    def _std_to_16bit(self, value: float, channel: AsphodelChannelInfo) -> int:
        try:
            if value <= 0:
                return 0

            std_max = (channel.maximum - channel.minimum) / 2.0

            if value >= std_max:
                return 0xFFFF

            return round((value / std_max) * 0xFFFF)
        except ValueError:
            return 0

    def _get_mean(self, modbus_index: int) -> Optional[tuple[float, int]]:
        try:
            channel_id, subchannel = self.modbus_index_channel[modbus_index]
        except KeyError:
            return None

        ringbuffer = self.mean_ringbuffers[channel_id]
        data = ringbuffer.get_contents()[:, subchannel]
        value = numpy.mean(data).item()
        return value, channel_id

    def get_mean_float(self, modbus_index: int) -> Optional[float]:
        result = self._get_mean(modbus_index)
        if result is None:
            return None
        return result[0]

    def get_mean_16bit(self, modbus_index: int) -> Optional[int]:
        result = self._get_mean(modbus_index)
        if result is None:
            return None
        value, channel_id = result
        channel_info = self.channel_info[channel_id].channel
        return self._mean_to_16bit(value, channel_info)

    def _get_std(self, modbus_index: int) -> Optional[tuple[float, int]]:
        try:
            channel_id, subchannel = self.modbus_index_channel[modbus_index]
        except KeyError:
            return None

        ringbuffer = self.mean_ringbuffers[channel_id]
        data = ringbuffer.get_contents()[:, subchannel]
        value = numpy.std(data).item()
        return value, channel_id

    def get_std_float(self, modbus_index: int) -> Optional[float]:
        result = self._get_std(modbus_index)
        if result is None:
            return None
        return result[0]

    def get_std_16bit(self, modbus_index: int) -> Optional[int]:
        result = self._get_std(modbus_index)
        if result is None:
            return None
        value, channel_id = result
        channel_info = self.channel_info[channel_id].channel
        return self._std_to_16bit(value, channel_info)

    def get_instant_float(self, modbus_index: int) -> Optional[float]:
        try:
            ringbuffer = self.instant_ringbuffers[modbus_index]
        except IndexError:
            return None

        data = ringbuffer.get_contents()
        if data.size != 0:
            value = numpy.mean(data).item()
            self.last_instant_value[modbus_index] = value
            ringbuffer.clear()
        else:
            value = self.last_instant_value[modbus_index]
        return value

    def get_instant_16bit(self, modbus_index: int) -> Optional[int]:
        value = self.get_instant_float(modbus_index)
        if value is None:
            return None
        channel_id, _subchannel = self.modbus_index_channel[modbus_index]
        channel_info = self.channel_info[channel_id].channel
        return self._mean_to_16bit(value, channel_info)


class ModbusSlave(IModbusSlaveContext):
    def __init__(self) -> None:
        super().__init__()

        self.float_encoder = struct.Struct("<f")
        self.int_encoder = struct.Struct("<i")
        self.decoder = struct.Struct("<HH")

        self.device_mappings: dict[str, tuple[int, ModbusDeviceMapping]] = {}
        self.device_intervals: dict[str, set[Interval]] = {}
        self.interval_tree: IntervalTree = IntervalTree()

    def add_device_mapping(self, serial_number: str, register_offset: int,
                           device_mapping: ModbusDeviceMapping) -> None:
        self.remove_device_mapping(serial_number)  # remove old one, if present

        t = (register_offset, device_mapping)

        self.device_mappings[serial_number] = t

        overlap_serials: set[str] = set()
        intervals: set[Interval] = set()

        for block in range(7):
            if block < 6:
                block_length = device_mapping.channel_count
            else:
                block_length = 2

            start_address = 1000 * block + register_offset
            end_address = start_address + (block_length * 2) - 1
            interval = Interval(start_address, end_address, t)
            intervals.add(interval)

            # find any other devices that overlap
            overlap_intervals: Iterable[Interval] = \
                self.interval_tree[start_address:end_address]
            for overlap_interval in overlap_intervals:
                overlapping_device_mapping = cast(ModbusDeviceMapping,
                                                  overlap_interval.data[1])
                overlap_serials.add(overlapping_device_mapping.serial_number)

            self.interval_tree.add(interval)

        self.device_intervals[serial_number] = intervals

        device_logger = DeviceLoggerAdapter(logger, serial_number)

        if overlap_serials:
            other_devices = ", ".join(sorted(overlap_serials))
            device_logger.warning("Modbus addresses overlap with: %s",
                                  other_devices)

        device_logger.info("Modbus starting (offset %s)", register_offset)

    def remove_device_mapping(self, serial_number: str) -> None:
        result = self.device_mappings.pop(serial_number, None)
        if result is None:
            return

        intervals = self.device_intervals.pop(serial_number)

        for interval in intervals:
            self.interval_tree.remove(interval)

        device_logger = DeviceLoggerAdapter(logger, serial_number)

        device_logger.info("Modbus stopping")

    def read_register_words(self, address: int) -> tuple[int, int]:
        try:
            intervals: list[Interval] = sorted(self.interval_tree[address])
            if not intervals:
                # no data or out of range: not an error
                return (0, 0)

            interval = intervals[0]
            register_offset, device_mapping = cast(
                tuple[int, ModbusDeviceMapping], interval.data)

            block_address = interval.begin - register_offset
            block = block_address // 1000
            index = (address - interval.begin) // 2

            if block == 0:
                # mean float
                value_float = device_mapping.get_mean_float(index)
                if value_float is None:
                    raise IndexError("Unknown index %s", index)
                else:
                    return cast(tuple[int, int], self.decoder.unpack(
                        self.float_encoder.pack(value_float)))
            elif block == 1:
                # mean 16bit
                value_16bit = device_mapping.get_mean_16bit(index)
                if value_16bit is None:
                    raise IndexError("Unknown index %s", index)
                else:
                    return (value_16bit, value_16bit)
            elif block == 2:
                # std float
                value_float = device_mapping.get_std_float(index)
                if value_float is None:
                    raise IndexError("Unknown index %s", index)
                else:
                    return cast(tuple[int, int], self.decoder.unpack(
                        self.float_encoder.pack(value_float)))
            elif block == 3:
                # std 16bit
                value_16bit = device_mapping.get_std_16bit(index)
                if value_16bit is None:
                    raise IndexError("Unknown index %s", index)
                else:
                    return (value_16bit, value_16bit)
            elif block == 4:
                # instant float
                value_float = device_mapping.get_instant_float(index)
                if value_float is None:
                    raise IndexError("Unknown index %s", index)
                else:
                    return cast(tuple[int, int], self.decoder.unpack(
                        self.float_encoder.pack(value_float)))
            elif block == 5:
                # instant 16bit
                value_16bit = device_mapping.get_instant_16bit(index)
                if value_16bit is None:
                    raise IndexError("Unknown index %s", index)
                else:
                    return (value_16bit, value_16bit)
            elif block == 6:
                if index == 0:
                    # serial number
                    value_32bit = device_mapping.numeric_serial
                    return cast(tuple[int, int], self.decoder.unpack(
                        self.int_encoder.pack(value_32bit)))
                elif index == 1:
                    # number of channels
                    value_32bit = device_mapping.channel_count
                    return cast(tuple[int, int], self.decoder.unpack(
                        self.int_encoder.pack(value_32bit)))
                else:
                    raise IndexError("Unknown index %s", index)
            else:
                raise IndexError("Unknown block %s", block)
        except Exception:
            logger.exception("Exception in read_register_words")
            return (0, 0)

    def reset(self) -> None:
        """ Resets all the datastores to their default values
        """
        pass

    def validate(self, fx: int, address: int, count: int = 1) -> bool:
        """ Validates the request to make sure it is in range

        :param fx: The function we are working with
        :param address: The starting address
        :param count: The number of values to test
        :returns: True if the request in within range, False otherwise
        """
        if self.decode(fx) in ['i', 'h']:
            return True
        return False

    def getValues(self, fx: int, address: int, count: int = 1) -> list[int]:
        """ Get `count` values from datastore

        :param fx: The function we are working with
        :param address: The starting address
        :param count: The number of values to retrieve
        :returns: The requested values from a:a+c
        """
        read_address = address & ~1
        if read_address != address:
            word_count = (count + 2) // 2
        else:
            word_count = (count + 1) // 2

        results: list[int] = []
        for i in range(word_count):
            words = self.read_register_words(read_address + i * 2)
            results.extend(words)

        if address != read_address:
            results = results[1:]

        results = results[:count]

        return results[:count]

    def setValues(self, fx: int, address: int, values: Any) -> None:
        """ Sets the datastore with the supplied values

        :param fx: The function we are working with
        :param address: The starting address
        :param values: The new values to be set
        """
        pass  # ignore any writes


class ModbusHandler:
    def __init__(self, preferences: Preferences):
        super().__init__()

        self.preferences = preferences

        self.stopped = False

        self.identity = ModbusDeviceIdentification()
        app = QtCore.QCoreApplication.instance()
        if app is not None:
            self.identity.VendorName = app.organizationName()
            self.identity.ProductCode = app.applicationName()
            self.identity.VendorUrl = app.organizationDomain()
            self.identity.ProductName = app.applicationName()
            self.identity.ModelName = app.applicationName()
            self.identity.MajorMinorRevision = app.applicationVersion()

        self.slave = ModbusSlave()
        self.context = ModbusServerContext(slaves=self.slave, single=True)

        self.modbus_server = None
        self.modbus_started = threading.Event()
        self.thread: Optional[threading.Thread] = None

        self.update_preferences()

    def stop(self) -> None:
        self.stopped = True
        self._stop_modbus()

    def join(self) -> None:
        if not self.stopped:
            self.stop()

        if self.thread is not None:
            self.thread.join()
            self.thread = None

    def stop_device(self, serial_number: str) -> None:
        self.slave.remove_device_mapping(serial_number)

    def get_device_callback(self, serial_number: str,
                            channel_info: dict[int, ChannelInformation]
                            ) -> Optional[DeviceCallback]:
        device_prefs = get_device_preferences(serial_number)

        if not device_prefs.modbus_enable:
            return None

        device_logger = DeviceLoggerAdapter(logger, serial_number)
        register_offset = device_prefs.modbus_register_offset

        if self.modbus_server is None:
            device_logger.warning("Modbus server not running")
            return None

        device_mapping = ModbusDeviceMapping(serial_number, channel_info)
        self.slave.add_device_mapping(serial_number, register_offset,
                                      device_mapping)

        return device_mapping.callback

    def update_preferences(self) -> None:
        if self.stopped:
            return

        address = ("", self.preferences.modbus_port)

        if self.preferences.modbus_enable:
            if self.modbus_server is None:
                self._start_modbus(address)
            else:
                if self.modbus_server.address != address:
                    # different address; restart
                    self._stop_modbus()
                    self._start_modbus(address)
        elif self.modbus_server is not None:
            self._stop_modbus()

    def _start_modbus(self, address: tuple[str, int]) -> None:
        if self.thread is not None:
            self.thread.join()
            self.thread = None

        try:
            self.modbus_server = ModbusTcpServer(
                self.context, ModbusSocketFramer, self.identity, address)
        except Exception:
            logger.exception("Error starting modbus server")
            self.modbus_server = None
            return

        self.modbus_started.clear()
        self.thread = threading.Thread(target=self._thread_run)
        self.thread.start()

        self.modbus_started.wait()

        logger.debug("Started modbus server on port %s", address[1])

    def _stop_modbus(self) -> None:
        if self.modbus_server:
            logger.debug("Stopping modbus server")
            self.modbus_server.shutdown()
            self.modbus_server = None

    def _thread_run(self) -> None:
        try:
            modbus_server: ModbusTcpServer = cast(
                ModbusTcpServer, self.modbus_server)
            self.modbus_started.set()
            modbus_server.serve_forever()
        except Exception:
            logger.exception("Uncaught exception in _thread_run")
            self._stop_modbus()
