import logging
from typing import Optional

from PySide6 import QtCore, QtWidgets

from asphodel.device_info import DeviceInfo
from hyperborea.setting_widget import SettingWidget

from .ui.ui_setting_dialog import Ui_SettingDialog

logger = logging.getLogger(__name__)


class SettingDialog(Ui_SettingDialog, QtWidgets.QDialog):
    def __init__(self, device_info: DeviceInfo,
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        # capture these now
        self.settings = device_info.settings
        self.nvm_bytes = device_info.nvm
        self.custom_enums = device_info.custom_enums
        self.setting_categories = device_info.setting_categories

        self.setting_widgets: list[SettingWidget] = []

        self.setupUi(self)  # type: ignore

        self.add_setting_widgets()

        b = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.RestoreDefaults)
        b.clicked.connect(self.restore_defaults)

    def add_setting_widgets(self) -> None:
        remaining_settings = set(range(len(self.settings)))

        setting_tabs: list[tuple[str,
                                 list[tuple[QtWidgets.QWidget, ...]]]] = []

        for name, category_settings in self.setting_categories:
            widgets: list[tuple[QtWidgets.QWidget, ...]] = []
            for setting_index in category_settings:
                if setting_index in remaining_settings:
                    remaining_settings.remove(setting_index)

                    setting = self.settings[setting_index]
                    widget = SettingWidget(setting, self.nvm_bytes,
                                           self.custom_enums)
                    self.setting_widgets.append(widget)
                    widgets.append(widget.widgets)
            setting_tabs.append((name, widgets))

        if remaining_settings:
            remaining_widgets: list[tuple[QtWidgets.QWidget, ...]] = []
            for setting_index in sorted(remaining_settings):
                setting = self.settings[setting_index]
                widget = SettingWidget(setting, self.nvm_bytes,
                                       self.custom_enums)
                self.setting_widgets.append(widget)
                remaining_widgets.append(widget.widgets)
            # add the default tab at the beginning
            setting_tabs.insert(0, ("Device Settings", remaining_widgets))

        for tab_name, widgets in setting_tabs:
            tab_widget = QtWidgets.QWidget()
            form_layout = QtWidgets.QFormLayout(tab_widget)

            for row_widgets in widgets:
                form_layout.addRow(*row_widgets)

            self.tabWidget.addTab(tab_widget, tab_name)

    def get_updated_nvm(self) -> bytes:
        nvm_bytes = bytearray(self.nvm_bytes)
        for widget in self.setting_widgets:
            widget.update_nvm(nvm_bytes)
        return bytes(nvm_bytes)

    @QtCore.Slot()
    def restore_defaults(self) -> None:
        for widget in self.setting_widgets:
            widget.restore_defaults()
