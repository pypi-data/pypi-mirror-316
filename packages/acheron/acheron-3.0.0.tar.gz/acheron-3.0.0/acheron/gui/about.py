import importlib
import logging
import sys
from typing import Optional

from PySide6 import QtWidgets

import asphodel

from .. import build_info

from .ui.ui_about import Ui_AboutDialog

logger = logging.getLogger(__name__)


class AboutDialog(Ui_AboutDialog, QtWidgets.QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        self.setupUi(self)  # type: ignore

        version = QtWidgets.QApplication.applicationVersion()

        label_str = self.tr("Version: {}").format(version)
        self.version.setText(label_str)

        build_date = build_info.get_build_date()
        if build_date:
            self.buildDate.setText(
                self.tr("Build Date: {}").format(build_date))
        else:
            self.buildDate.setVisible(False)

        self.update_library_versions()

        self.layout().setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetFixedSize)

    def get_version(self, library: str) -> str:
        try:
            lib = importlib.import_module(library)
            return lib.__version__
        except (AttributeError, ImportError):
            return "ERROR"

    def update_library_versions(self) -> None:
        libraries = ["boto3", "diskcache", "hyperborea", "numpy", "psutil",
                     "pymodbus", "pyqtgraph", "PySide6", "requests",
                     "serial", "setproctitle"]
        vers = {}
        for lib in libraries:
            vers[lib] = self.get_version(lib)

        # special case for asphodel and asphodel_py
        vers["asphodel_py"] = self.get_version("asphodel")
        vers["asphodel"] = asphodel.build_info

        # python version (sys.version is too long)
        is_64bit = sys.maxsize > (2 ** 32)
        bit_str = "64 bit" if is_64bit else "32 bit"
        python_ver = ".".join(map(str, sys.version_info[:3]))
        python_str = "{} ({} {})".format(python_ver, sys.platform, bit_str)
        vers['python'] = python_str

        s = "\n".join(k + ": " + vers[k] for k in sorted(vers, key=str.lower))
        self.libraryVersions.setText(s)
