#!/usr/bin/env python3
import logging
import sys

from PySide6 import QtCore

import asphodel
from ..device_process.proxy import DeviceProxyManager

from acheron import force_exit, main_init, __version__
from acheron.logging import setup_logging
from acheron.core.dispatcher import Dispatcher
from acheron.core.preferences import create_empty_settings, Preferences
from acheron.disk.schedule_reader import ScheduleReader

logger = logging.getLogger(__name__)


MAIN_PROCESS_NAME = "acheron-cli"
DEVICE_PROCESS_NAME = "acheron-device"
CALC_PROCESS_NAME = "acheron-calc"


def main() -> None:
    # NOTE: this call MUST be first, because of multiprocessing
    main_init(MAIN_PROCESS_NAME)

    app = QtCore.QCoreApplication(sys.argv)
    app.setApplicationName("Acheron")
    app.setOrganizationDomain("suprocktech.com")
    app.setOrganizationName("Suprock Tech")

    app.setApplicationVersion(__version__)

    setup_logging(console=True)
    create_empty_settings()

    # periodically go into the python interpreter from Qt for SIGINT handling
    timer = QtCore.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    logger.info("Acheron started (Version {})".format(__version__))

    try:
        missing_funcs = asphodel.nativelib.missing_funcs
    except AttributeError:
        missing_funcs = []  # to bypass the next warning
        message = "Asphodel python mismatch!"
        logging.warning(message)

    if missing_funcs:
        missing_str = ", ".join(sorted(missing_funcs))
        logging.warning("Missing Asphodel functions: {}".format(missing_str))

    proxy_manager = DeviceProxyManager(DEVICE_PROCESS_NAME)

    preferences = Preferences()
    dispatcher = Dispatcher(proxy_manager, preferences, CALC_PROCESS_NAME)

    schedule_path = QtCore.QStandardPaths.writableLocation(
        QtCore.QStandardPaths.StandardLocation.AppLocalDataLocation)
    schedule_reader = ScheduleReader(schedule_path, dispatcher)
    schedule_reader.start()

    app.exec()

    logger.info("Acheron exiting")

    schedule_reader.stop()
    dispatcher.stop()
    proxy_manager.stop()
    dispatcher.join()

    logger.info("Acheron finished")

    force_exit()


if __name__ == '__main__':
    main()
