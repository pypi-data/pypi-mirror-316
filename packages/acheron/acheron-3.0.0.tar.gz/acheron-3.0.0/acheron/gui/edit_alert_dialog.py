import logging
import math
from typing import Optional

from PySide6 import QtWidgets

import asphodel

from ..calc_process.types import LimitType

from .ui.ui_edit_alert_dialog import Ui_EditAlertDialog

logger = logging.getLogger(__name__)


class EditAlertDialog(Ui_EditAlertDialog, QtWidgets.QDialog):
    def __init__(self, alert_limits: dict[LimitType, float],
                 unit_formatter: asphodel.AsphodelNativeUnitFormatter,
                 parent: Optional[QtWidgets.QWidget] = None):
        self.unit_formatter = unit_formatter

        super().__init__(parent)

        self.setupUi(self)  # type: ignore
        self.extra_ui_setup(alert_limits)

    def extra_ui_setup(self, alert_limits: dict[LimitType, float]) -> None:
        mean_formatter = asphodel.nativelib.create_custom_unit_formatter(
            self.unit_formatter.conversion_scale,
            self.unit_formatter.conversion_offset,
            0.0,
            self.unit_formatter.unit_ascii,
            self.unit_formatter.unit_utf8,
            self.unit_formatter.unit_html
        )

        std_formatter = asphodel.nativelib.create_custom_unit_formatter(
            self.unit_formatter.conversion_scale,
            0.0,
            0.0,
            self.unit_formatter.unit_ascii,
            self.unit_formatter.unit_utf8,
            self.unit_formatter.unit_html
        )

        self.meanHigh.set_unit_formatter(mean_formatter)
        self.meanLow.set_unit_formatter(mean_formatter)
        self.stdHigh.set_unit_formatter(std_formatter)
        self.stdLow.set_unit_formatter(std_formatter)

        self.meanHigh.setMaximum(math.inf)
        self.meanHigh.setMinimum(-math.inf)
        self.meanLow.setMaximum(math.inf)
        self.meanLow.setMinimum(-math.inf)
        self.stdHigh.setMaximum(math.inf)
        self.stdHigh.setMinimum(0.0)
        self.stdLow.setMaximum(math.inf)
        self.stdLow.setMinimum(0.0)

        self.limit_type_widgets = (
            (LimitType.MEAN_HIGH_LIMIT, self.meanHighEnabled, self.meanHigh),
            (LimitType.MEAN_LOW_LIMIT, self.meanLowEnabled, self.meanLow),
            (LimitType.STD_HIGH_LIMIT, self.stdHighEnabled, self.stdHigh),
            (LimitType.STD_LOW_LIMIT, self.stdLowEnabled, self.stdLow),
        )

        for limit_type, enabled, spinbox in self.limit_type_widgets:
            value = alert_limits.get(limit_type)
            if value is not None:
                spinbox.setValue(value)
            enabled.setChecked(value is not None)

    def get_alert_limits(self) -> dict[LimitType, float]:
        alert_limits: dict[LimitType, float] = {}
        for limit_type, enabled, spinbox in self.limit_type_widgets:
            if enabled.isChecked():
                alert_limits[limit_type] = spinbox.value()

        return alert_limits
