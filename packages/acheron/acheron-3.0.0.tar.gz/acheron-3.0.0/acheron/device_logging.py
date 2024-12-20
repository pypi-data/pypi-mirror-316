import logging
from typing import Optional


class OptionalDeviceStringFilter(logging.Filter):
    # creates a record.optdevice string created via fmt % record.device
    # but replaces it with fallback if record.device does not exist
    def __init__(self, fmt: str, fallback: str):
        self.fmt = fmt
        self.fallback = fallback

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            record.optdevice = self.fmt % record.proxy_string  # type: ignore
        except AttributeError:
            record.optdevice = self.fallback
        return True


class DeviceLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger: logging.Logger, serial_number: str,
                 proxy_string: Optional[str] = None):
        if not proxy_string:
            proxy_string = serial_number
        super().__init__(logger, {'serial_number': serial_number,
                                  "proxy_string": proxy_string})


class RemoteToLocalLogHandler(logging.Handler):
    def __init__(self, logger_name: str):
        super().__init__()
        self.logger = logging.getLogger(logger_name)

    def emit(self, record: logging.LogRecord) -> None:
        self.logger.handle(record)
