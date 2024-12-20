import functools
import logging
import selectors
import socket
import threading
import time
from typing import Optional

import numpy
from numpy.typing import NDArray

from .connectivity_manager import DeviceCallback
from ..calc_process.types import ChannelInformation
from ..core.preferences import get_device_preferences, Preferences
from ..device_logging import DeviceLoggerAdapter

logger = logging.getLogger(__name__)


class DeviceSocketTransmitter:
    def __init__(self, socket_buffer_size: int,
                 channel_ports: dict[tuple[int, int], int],
                 selector: selectors.BaseSelector,
                 logger: DeviceLoggerAdapter):
        self.socket_buffer_size = socket_buffer_size
        self.channel_ports = channel_ports
        self.selector = selector
        self.logger = logger

        self.lock = threading.Lock()
        self.listen_sockets: set[socket.socket] = set()
        self.all_channel_sockets: dict[int, list[
            tuple[int, socket.socket]]] = {}

        for (channel_id, subchannel_index), port in channel_ports.items():
            try:
                # create a TCP socket
                listen_sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
                listen_sock.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                listen_sock.setblocking(False)
                listen_sock.bind(("", port))
                listen_sock.listen()

                accept_cb = functools.partial(self._accept_ready, channel_id,
                                              subchannel_index, listen_sock)
                self.selector.register(
                    listen_sock, selectors.EVENT_READ, accept_cb)

                self.logger.info(f"Listening for connections on port {port}")

                self.listen_sockets.add(listen_sock)
            except Exception:
                self.logger.exception("Error opening socket on port %s",
                                      port)

    def stop(self) -> None:
        self.logger.debug("Stopping transmitting sockets")

        with self.lock:
            for listen_sock in self.listen_sockets:
                if listen_sock:
                    try:
                        self.selector.unregister(listen_sock)
                    except KeyError:
                        pass  # ignure, selector must already be closed
                    listen_sock.close()
            self.listen_sockets.clear()

            for channel_id, sockets in self.all_channel_sockets.items():
                for subchannel_index, connected_sock in sockets:
                    try:
                        self.selector.unregister(connected_sock)
                    except KeyError:
                        pass  # ignure, selector must already be closed

                    port = self.channel_ports[(channel_id, subchannel_index)]

                    connected_sock.close()

                    self.logger.info("Connection closed on %s", port)
            self.all_channel_sockets.clear()

    def _accept_ready(self, channel_id: int, subchannel_index: int,
                      listen_sock: socket.socket) -> None:
        key = (channel_id, subchannel_index)
        try:
            port = self.channel_ports[key]

            connected_sock, _addr = listen_sock.accept()  # Should be ready

            self.logger.info("Accepted new connection on port %s", port)

            connected_sock.setblocking(False)
            connected_sock.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

            if self.socket_buffer_size != 0:
                default_buffer_size = connected_sock.getsockopt(
                    socket.SOL_SOCKET, socket.SO_SNDBUF)
                if self.socket_buffer_size > default_buffer_size:
                    connected_sock.setsockopt(
                        socket.SOL_SOCKET, socket.SO_SNDBUF,
                        self.socket_buffer_size)
                    new_buffer_size = connected_sock.getsockopt(
                        socket.SOL_SOCKET, socket.SO_SNDBUF)
                    if new_buffer_size != self.socket_buffer_size:
                        self.logger.warning(
                            "Socket buffer is %s not requested %s",
                            new_buffer_size, self.socket_buffer_size)
                    else:
                        self.logger.debug("Socket buffer size is %s",
                                          new_buffer_size)
                else:
                    self.logger.debug("Socket buffer size is OS default %s",
                                      default_buffer_size)

            close_cb = functools.partial(self._close_socket, channel_id,
                                         subchannel_index, connected_sock)

            # any read event means to close the socket
            self.selector.register(
                connected_sock, selectors.EVENT_READ, close_cb)

            with self.lock:
                try:
                    channel_sockets = self.all_channel_sockets[channel_id]
                except KeyError:
                    channel_sockets = []
                    self.all_channel_sockets[channel_id] = channel_sockets
                channel_sockets.append((subchannel_index, connected_sock))
        except OSError:
            pass
        except Exception:
            self.logger.exception("Unhandled exception in _accept_ready()")

    def _close_socket(self, channel_id: int, subchannel_index: int,
                      connected_sock: socket.socket) -> None:
        try:
            self.selector.unregister(connected_sock)
        except Exception:
            pass  # ignore, selector might be closed or socket may be closed

        with self.lock:
            channel_sockets = self.all_channel_sockets.get(channel_id)
            if channel_sockets:
                channel_sockets.remove((subchannel_index, connected_sock))

        port = self.channel_ports[(channel_id, subchannel_index)]

        try:
            connected_sock.close()
        except Exception:
            pass  # ignore, socket may be closed already

        self.logger.info("Connection closed on %s", port)

    def callback(self, channel_id: int, data: NDArray[numpy.float64]) -> None:
        data = data.astype("<f8")

        with self.lock:
            channel_sockets = self.all_channel_sockets.get(channel_id)

        if channel_sockets is None:
            return  # don't care about this data

        for subchannel_index, sock in channel_sockets:
            try:
                socket_bytes = data[:, subchannel_index].tobytes()
                sent = sock.send(socket_bytes)
            except Exception:
                # error on this socket
                self._close_socket(channel_id, subchannel_index, sock)
                continue
            if sent != len(socket_bytes):
                # other end couldn't keep up
                self._close_socket(channel_id, subchannel_index, sock)


class SocketHandler:
    def __init__(self, preferences: Preferences):
        super().__init__()

        self.preferences = preferences

        self.socket_transmitters: dict[str, DeviceSocketTransmitter] = {}
        self.device_ports: dict[str, set[int]] = {}
        self.used_ports: dict[int, str] = {}  # value serial number

        self.selector = selectors.DefaultSelector()

        self.finished = threading.Event()
        self.selector_thread = threading.Thread(target=self._selector_loop)
        self.selector_thread.start()

    def stop(self) -> None:
        self.finished.set()

        for socket_transmitter in self.socket_transmitters.values():
            socket_transmitter.stop()
        self.socket_transmitters.clear()
        self.device_ports.clear()
        self.used_ports.clear()

    def join(self) -> None:
        self.selector_thread.join()

    def update_preferences(self) -> None:
        pass  # not needed in this implementation

    def stop_device(self, serial_number: str) -> None:
        socket_transmitter = self.socket_transmitters.pop(serial_number, None)
        if socket_transmitter:
            socket_transmitter.stop()

        ports = self.device_ports.pop(serial_number, None)
        if ports:
            for port in ports:
                del self.used_ports[port]

    def get_device_callback(self, serial_number: str,
                            channel_info: dict[int, ChannelInformation]
                            ) -> Optional[DeviceCallback]:

        socket_transmitter = self.socket_transmitters.get(serial_number)
        if socket_transmitter:
            return socket_transmitter.callback

        device_logger = DeviceLoggerAdapter(logger, serial_number)
        device_prefs = get_device_preferences(serial_number)
        desired_channel_ports = device_prefs.get_all_channel_ports()
        channel_ports: dict[tuple[int, int], int] = {}

        for (channel_id, subchannel_id), port in desired_channel_ports.items():
            other_device = self.used_ports.get(port)
            if other_device:
                device_logger.warning("Port %s already in use by %s!",
                                      port, other_device)
                continue

            info = channel_info.get(channel_id)
            if not info:
                # channel doesn't exist (at the moment)
                continue

            subchannel_count = len(info.subchannel_names)
            if subchannel_id >= subchannel_count:
                # subchannel doesn't exist (at the moment)
                continue

            channel_ports[(channel_id, subchannel_id)] = port
            self.used_ports[port] = serial_number

        if not channel_ports:
            return None

        self.device_ports[serial_number] = set(channel_ports.values())

        socket_transmitter = DeviceSocketTransmitter(
            self.preferences.socket_buffer_size, channel_ports, self.selector,
            device_logger)
        self.socket_transmitters[serial_number] = socket_transmitter
        return socket_transmitter.callback

    def _selector_loop(self) -> None:
        try:
            selector_map = self.selector.get_map()
            while not self.finished.is_set():
                if len(selector_map) == 0:
                    # no sockets open yet
                    time.sleep(0.1)
                else:
                    events = self.selector.select(timeout=0.1)
                    for key, _mask in events:
                        callback = key.data
                        callback()
        except Exception:
            logger.exception("Uncaught exception in selector_loop")
            self.stop()
        finally:
            self.selector.close()
