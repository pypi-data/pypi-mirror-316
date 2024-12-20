import logging
from typing import Optional

from PySide6 import QtCore, QtNetwork

logger = logging.getLogger(__name__)


class SingleAppInstance(QtCore.QObject):
    focus_request = QtCore.Signal()
    url_request = QtCore.Signal(str)

    def __init__(self, instance_id: str):
        super().__init__()
        self.instance_id = instance_id

        self._out_stream: Optional[QtCore.QTextStream] = None
        self._in_socket: Optional[QtNetwork.QLocalSocket] = None
        self._in_stream: Optional[QtCore.QTextStream] = None

        # Is there another instance running?
        self._out_socket: Optional[QtNetwork.QLocalSocket] = \
            QtNetwork.QLocalSocket()
        self._out_socket.connectToServer(self.instance_id)
        self.already_running = self._out_socket.waitForConnected()

        if self.already_running:
            self._out_stream = QtCore.QTextStream(self._out_socket)
        else:
            # this is the first instance
            self._out_socket = None
            self._server = QtNetwork.QLocalServer()
            self._server.listen(self.instance_id)
            self._server.newConnection.connect(self._new_connection_cb)

    def close(self) -> None:
        if self._out_socket:
            self._out_socket.close()
            self._out_socket = None
        if self._in_socket:
            self._in_socket.close()
            self._in_socket = None

    def _send_message(self, msg: str) -> None:
        if not self._out_stream or not self._out_socket:
            raise RuntimeError("this is the main process")

        _ = self._out_stream << msg << '\n'
        self._out_stream.flush()
        self._out_socket.waitForBytesWritten()

    def send_url_request(self, url: str) -> None:
        self._send_message(url)
        logger.debug("Sent url request to main process: %s", url)

    def send_focus_request(self) -> None:
        self._send_message("focus")
        logger.debug("Sent focus request to main process")

    @QtCore.Slot()
    def _new_connection_cb(self) -> None:
        if self._in_socket:
            self._in_socket.readyRead.disconnect(self._ready_read_cb)
        self._in_socket = self._server.nextPendingConnection()
        if not self._in_socket:
            return
        self._in_stream = QtCore.QTextStream(self._in_socket)
        self._in_socket.readyRead.connect(self._ready_read_cb)

    @QtCore.Slot()
    def _ready_read_cb(self) -> None:
        if self._in_stream is None:
            return

        while True:
            msg = self._in_stream.readLine()
            if not msg:
                break
            elif msg == "focus":
                logger.debug("Received focus request in main process")
                self.focus_request.emit()
            else:
                # assume it's a url request
                logger.debug("Received url requset in main process: %s", msg)
                self.url_request.emit(msg)
