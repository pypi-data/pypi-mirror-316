from collections import deque
import logging
import logging.handlers
import threading
from typing import Any, Optional, Union

from PySide6 import QtCore

logger = logging.getLogger(__name__)

GUI_LOG_SIZE = 1000


class GUILogModel(QtCore.QAbstractListModel):
    def __init__(self, global_deque: deque[str]):
        super().__init__()

        self.list = list(global_deque)
        self.deque: deque[str] = deque(maxlen=GUI_LOG_SIZE)
        self.lock = threading.Lock()

    def log_message(self, message: str) -> None:
        with self.lock:
            self.deque.append(message)

    def update_messages(self) -> None:
        with self.lock:
            new_messages = list(self.deque)
            if not new_messages:
                return
            self.deque.clear()
        messages_len = len(new_messages)
        remove_count = messages_len + len(self.list) - GUI_LOG_SIZE
        if remove_count > 0:
            self.beginRemoveRows(QtCore.QModelIndex(), 0, remove_count - 1)
            del self.list[0:remove_count]
            self.endRemoveRows()

        first = len(self.list)
        last = first + messages_len - 1
        self.beginInsertRows(QtCore.QModelIndex(), first, last)
        self.list.extend(new_messages)
        self.endInsertRows()

        self.dataChanged.emit(first, last)

    def rowCount(self, parent: Any = None) -> int:
        return len(self.list)

    def data(self, index: Union[QtCore.QModelIndex,
                                QtCore.QPersistentModelIndex],
             role: int = 0) -> Optional[str]:
        row = index.row()
        if row < 0 or row >= len(self.list):
            return ""

        if (role == QtCore.Qt.ItemDataRole.DisplayRole or
                role == QtCore.Qt.ItemDataRole.EditRole):
            return self.list[row]
        else:
            return None


_models: dict[str, GUILogModel] = {}
_global_deque: deque[str] = deque(maxlen=GUI_LOG_SIZE)


class GUILogHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_cb)
        self.timer.start(20)

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        try:
            serial_number = record.serial_number  # type: ignore
            try:
                model = _models[serial_number]
            except KeyError:
                model = GUILogModel(_global_deque)
                _models[serial_number] = model
            model.log_message(message)
        except AttributeError:
            # global log message
            _global_deque.append(message)
            for model in _models.values():
                model.log_message(message)

    @QtCore.Slot()
    def timer_cb(self) -> None:
        for serial_number, model in _models.items():
            model.update_messages()


def get_log_list_model(serial_number: str) -> QtCore.QAbstractItemModel:
    try:
        model = _models[serial_number]
    except KeyError:
        model = GUILogModel(_global_deque)
        _models[serial_number] = model
    return model
