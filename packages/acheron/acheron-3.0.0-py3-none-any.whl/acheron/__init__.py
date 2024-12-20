#!/usr/bin/env python3
import setproctitle  # NOTE: this should be first!

import ctypes
import logging
import multiprocessing
import os
import signal
import sys
from typing import Any

logger = logging.getLogger(__name__)


try:
    from .version import version as __version__
except ImportError:
    __version__ = "UNKNOWN"


def main_is_frozen() -> bool:
    """Return True if the script is frozen, False otherwise."""
    return getattr(sys, 'frozen', False)


def force_exit() -> None:
    # based on pyqtgraph.exit, with fix for macos

    # # invoke atexit callbacks
    import atexit
    atexit._run_exitfuncs()

    # # close file handles
    if sys.platform == 'darwin':
        # trying to close 7 produces an illegal instruction on the Mac
        os.closerange(3, 7)
        os.closerange(8, 4096)
    else:
        os.closerange(3, 4096)  # just guessing on the maximum descriptor count

    os._exit(0)


def shutdown_signal(*args: Any) -> None:
    from PySide6 import QtCore
    QtCore.QCoreApplication.quit()


def main_init(main_process_title: str) -> None:
    # freeze_support() MUST be first. Anything before this will cease to exist
    multiprocessing.freeze_support()

    # spawn is only option on windows, linux needs spawn or forkserver to work
    multiprocessing.set_start_method("spawn")

    setproctitle.setproctitle(main_process_title)

    if main_is_frozen():
        # work around for botocore data
        cacert = os.path.join(os.path.dirname(sys.executable), 'botodata',
                              'cacert.pem')
        os.environ["AWS_CA_BUNDLE"] = cacert
        botodata = os.path.join(os.path.dirname(sys.executable), 'botodata')
        os.environ["AWS_DATA_PATH"] = botodata

    elif sys.platform == 'win32':
        # show correct windows taskbar icon when running not frozen
        myappid = u'com.sprocktech.' + main_process_title + '.' + __version__
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    if not sys.stdout or not sys.stderr:
        sys.stdout = open(os.devnull)
        sys.stderr = open(os.devnull)

    # force the settings to use an INI file instead of the registry
    from PySide6 import QtCore
    QtCore.QSettings.setDefaultFormat(QtCore.QSettings.Format.IniFormat)

    # allow program to be closed gracefully
    signal.signal(signal.SIGINT, shutdown_signal)  # ctrl+c
    signal.signal(signal.SIGTERM, shutdown_signal)


if __name__ == '__main__':
    from .gui import __main__
    __main__.main()
