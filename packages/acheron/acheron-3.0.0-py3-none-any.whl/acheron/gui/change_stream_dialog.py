import logging
from typing import Optional

from PySide6 import QtWidgets

import asphodel

from .ui.ui_change_stream_dialog import Ui_ChangeStreamDialog

logger = logging.getLogger(__name__)


class ChangeStreamDialog(Ui_ChangeStreamDialog, QtWidgets.QDialog):
    def __init__(self, streams: list[asphodel.AsphodelStreamInfo],
                 channels: list[asphodel.AsphodelChannelInfo],
                 active_streams: frozenset[int],
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.streams = streams
        self.channels = channels
        self.active_streams = active_streams

        self.check_boxes: dict[int, QtWidgets.QCheckBox] = {}

        self.setupUi(self)  # type: ignore

        self.add_check_boxes()

    def add_check_boxes(self) -> None:
        d = {}  # key: min(channel index), value: check box

        for index, stream in enumerate(self.streams):
            check_box = QtWidgets.QCheckBox(self)
            check_box.setChecked(index in self.active_streams)
            self.check_boxes[index] = check_box

            stream_channels = stream.channel_index_list[:stream.channel_count]

            channel_names = []
            for ch_index in stream_channels:
                channel = self.channels[ch_index]
                channel_names.append(channel.name.decode("utf-8"))

            stream_text = "Stream {} ({})".format(index,
                                                  ", ".join(channel_names))

            check_box.setText(stream_text)

            d[min(stream_channels)] = check_box

        for ch_index in sorted(d.keys()):
            check_box = d[ch_index]
            self.verticalLayout.addWidget(check_box)

    def get_new_stream_list(self) -> Optional[list[int]]:
        all_true = True

        stream_list: list[int] = []

        for index in sorted(self.check_boxes.keys()):
            check_box = self.check_boxes[index]
            if check_box.isChecked():
                stream_list.append(index)
            else:
                all_true = False

        if all_true:
            return None
        else:
            return stream_list
