import logging
from logging.handlers import QueueListener
import multiprocessing
from multiprocessing.connection import Connection
import threading
from typing import Any, Optional

from PySide6 import QtCore

from hyperborea.namedprocess import NamedProcess
from ..device_logging import DeviceLoggerAdapter, RemoteToLocalLogHandler

from .remote import run_calc_runner
from .types import CalcControl, CalcData, CalcSettings, Trigger

logger = logging.getLogger(__name__)


class CalcProcess(QtCore.QObject):
    # device_info, active_streams, channel_info
    processing_start = QtCore.Signal(object, object, object)

    processing_stop = QtCore.Signal()

    # error_str
    status_received = QtCore.Signal(object)

    # channel_id, mean, std
    channel_update = QtCore.Signal(object, object, object)

    # channel_id, time_array, data_array
    plot_update = QtCore.Signal(object, object, object)

    # channel_id, subchannel_id, fft_freqs, fft_data
    # NOTE: data may be a scalar from 0 to 1 showing buffering status
    fft_update = QtCore.Signal(object, object, object, object)

    # total, last_datetime, recent
    lost_packet_update = QtCore.Signal(object, object, object)

    # stream_id
    unknown_id = QtCore.Signal(object)

    # active_triggers: set[str]
    active_triggers_changed = QtCore.Signal(object)

    # internal use only
    _start_plot_update = QtCore.Signal(int)
    _start_fft_update = QtCore.Signal(int)

    def __init__(self, calc_process_name: str, serial: str, is_shown: bool,
                 settings: CalcSettings, triggers: set[Trigger]):
        super().__init__()

        self.log_queue: "multiprocessing.Queue" = multiprocessing.Queue()
        local_handler = RemoteToLocalLogHandler(__name__ + ".remote")
        self.log_listener = QueueListener(self.log_queue, local_handler)
        self.log_listener.start()

        self.logger = DeviceLoggerAdapter(logger, serial)

        self.lock = threading.Lock()
        self.stopped = threading.Event()
        self.finished = threading.Event()
        self.closed = threading.Event()

        self.plot_data: Optional[tuple] = None
        self.fft_data: Optional[tuple] = None
        self.plot_timer = QtCore.QTimer(self)
        self.plot_timer.setSingleShot(True)
        self.plot_timer.timeout.connect(self._plot_update_cb)
        self._start_plot_update.connect(self.plot_timer.start)
        self.fft_timer = QtCore.QTimer(self)
        self.fft_timer.setSingleShot(True)
        self.fft_timer.timeout.connect(self._fft_update_cb)
        self._start_fft_update.connect(self.fft_timer.start)

        # for the StreamController communication
        self.status_rx_pipe, self.status_tx_pipe = multiprocessing.Pipe(False)
        self.packet_rx_pipe, self.packet_tx_pipe = multiprocessing.Pipe(False)
        self.stream_ctrl_rx_pipe, self.stream_ctrl_tx_pipe = \
            multiprocessing.Pipe(False)

        # for the CalcRunner communication
        self.data_rx_pipe, self.data_tx_pipe = multiprocessing.Pipe(False)
        self.calc_ctrl_rx_pipe, self.calc_ctrl_tx_pipe = multiprocessing.Pipe(
            False)

        self.status_thread = threading.Thread(target=self.status_thread_run)
        self.status_thread.start()

        self.data_thread = threading.Thread(target=self.data_thread_run)
        self.data_thread.start()

        self.remote_process = NamedProcess(
            name=calc_process_name,
            description=serial,
            target=run_calc_runner,
            args=(self.log_queue, self.packet_rx_pipe, self.data_tx_pipe,
                  self.calc_ctrl_rx_pipe, serial, is_shown, settings,
                  triggers))
        self.remote_process.daemon = True
        self.remote_process.start()

    def stop(self) -> None:
        with self.lock:
            if not self.stopped.is_set():
                self.stopped.set()
                self.calc_ctrl_tx_pipe.send((CalcControl.STOP, ))
                self.logger.debug("Calc process stopping")

    @QtCore.Slot()
    def close(self) -> None:
        """Called after the stream controller has been stopped"""

        self.stop()

        with self.lock:
            if self.closed.is_set():
                # this check should help if close() is called after join()
                return

            self.calc_ctrl_tx_pipe.send((CalcControl.CLOSE, ))
            self.finished.set()

            if self.log_listener:
                self.log_listener.stop()
                self.log_listener = None  # type: ignore
                self.log_queue.close()
                self.log_queue = None  # type: ignore

            self.closed.set()

            self.logger.debug("Calc process closed")

    def join(self) -> None:
        self.close()

        self.remote_process.join()
        self.data_thread.join()
        self.status_thread.join()

        # close both sides of the pipe, because the GC will do it anyway
        self.status_rx_pipe.close()
        self.status_tx_pipe.close()
        self.packet_rx_pipe.close()
        self.packet_tx_pipe.close()
        self.stream_ctrl_rx_pipe.close()
        self.stream_ctrl_tx_pipe.close()
        self.data_rx_pipe.close()
        self.data_tx_pipe.close()
        self.calc_ctrl_rx_pipe.close()
        self.calc_ctrl_tx_pipe.close()

        self.logger.debug("Calc process joined")

    def get_pipes(self) -> tuple[Connection, Connection, Connection]:
        return (self.stream_ctrl_rx_pipe, self.packet_tx_pipe,
                self.status_tx_pipe)  # type: ignore

    def status_thread_run(self) -> None:
        try:
            pipe = self.status_rx_pipe
            while True:
                if self.finished.is_set():
                    break

                if pipe.poll(0.1):  # 100 ms
                    try:
                        status = pipe.recv()
                    except EOFError:
                        break

                    if status is None:
                        break

                    self.status_received.emit(status)
        except Exception:
            self.logger.exception("Unhandled exception in status_thread_run")
            self.stop()

    def data_thread_run(self) -> None:
        try:
            pipe = self.data_rx_pipe
            while True:
                if self.finished.is_set():
                    break

                if pipe.poll(0.1):  # 100 ms
                    try:
                        data = pipe.recv()
                    except EOFError:
                        break

                    self.handle_data(data)
        except Exception:
            self.logger.exception("Unhandled exception in data_thread_run")
            self.stop()

    def handle_data(self, data: tuple[Any, ...]) -> None:
        if self.stopped.is_set():
            return

        if data[0] == CalcData.PROCESSING_START:
            self.processing_start.emit(*data[1:])
        elif data[0] == CalcData.PROCESSING_STOP:
            self.processing_stop.emit(*data[1:])
        elif data[0] == CalcData.CHANNEL_UPDATE:
            self.channel_update.emit(*data[1:])
        elif data[0] == CalcData.PLOT_UPDATE:
            self.plot_data = data[1:]
            self._start_plot_update.emit(1)
        elif data[0] == CalcData.FFT_UPDATE:
            self.fft_data = data[1:]
            self._start_fft_update.emit(1)
        elif data[0] == CalcData.LOST_PACKET_UPDATE:
            self.lost_packet_update.emit(*data[1:])
        elif data[0] == CalcData.UNKNOWN_ID:
            self.unknown_id.emit(*data[1:])
        elif data[0] == CalcData.ACTIVE_TRIGGERS_CHANGED:
            self.active_triggers_changed.emit(*data[1:])

    def set_is_shown(self, is_shown: bool) -> None:
        self.calc_ctrl_tx_pipe.send((CalcControl.SET_SHOWN, is_shown))

    def plot_change(self, channel_id: Optional[int],
                    subchannel_index: Optional[int]) -> None:
        self.calc_ctrl_tx_pipe.send(
            (CalcControl.PLOT_CHANGE, channel_id, subchannel_index))

    def reset_lost_packets(self) -> None:
        self.calc_ctrl_tx_pipe.send((CalcControl.RESET_LOST_PACKETS, ))

    def send_stream_ctrl_message(self, message: tuple[Any, ...]) -> None:
        self.stream_ctrl_tx_pipe.send(message)

    def change_settings(self, settings: CalcSettings) -> None:
        self.calc_ctrl_tx_pipe.send((CalcControl.CHANGE_SETTINGS, settings))

    def change_triggers(self, triggers: set[Trigger]) -> None:
        self.calc_ctrl_tx_pipe.send((CalcControl.CHANGE_TRIGGERS, triggers))

    def set_connectivity_pipe(self, pipe: Connection) -> None:
        self.calc_ctrl_tx_pipe.send((CalcControl.SET_CONNECTIVITY_PIPE, pipe))

    @QtCore.Slot()
    def _plot_update_cb(self) -> None:
        data = self.plot_data
        self.plot_data = None

        if data:
            self.plot_update.emit(*data)

    @QtCore.Slot()
    def _fft_update_cb(self) -> None:
        data = self.fft_data
        self.fft_data = None

        if data:
            self.fft_update.emit(*data)
