import collections
import datetime
from dataclasses import dataclass
import email.message
import email.utils
import logging
import smtplib
import time
import threading
from typing import Callable, Optional

from ..device_logging import DeviceLoggerAdapter

from ..calc_process.types import Trigger
from ..core.preferences import Preferences

logger = logging.getLogger(__name__)


EmailCallback = Callable[[Optional[Exception]], None]


@dataclass(eq=True, frozen=True)
class AlertInfo:
    serial_number: str
    display_name: str
    trigger_list: list[tuple[Trigger, str]]  # trigger, subchannel_name
    dt: datetime.datetime


@dataclass(frozen=True)
class EmailSettings:
    from_address: str
    to_address: str
    smtp_host: str
    smtp_port: int
    security: str
    use_auth: bool
    smtp_user: str
    smtp_password: str


def preferences_to_email_settings(preferences: Preferences) -> EmailSettings:
    return EmailSettings(
        from_address=preferences.alert_from_address,
        to_address=preferences.alert_to_address,
        smtp_host=preferences.alert_smtp_host,
        smtp_port=preferences.alert_smtp_port,
        security=preferences.alert_security.lower(),
        use_auth=preferences.alert_use_auth,
        smtp_user=preferences.alert_smtp_user,
        smtp_password=preferences.alert_smtp_password,
    )


def validate_email_settings(email_settings: EmailSettings) -> None:
    if email_settings.security not in ['', 'starttls', 'ssl']:
        raise ValueError(
            f'unknown security setting "{email_settings.security}"')

    if email_settings.from_address == '':
        raise ValueError('no email from address')

    if email_settings.to_address == '':
        raise ValueError('no email to address')


def _get_smtp_object(email_settings: EmailSettings) -> smtplib.SMTP:
    security = email_settings.security
    smtp_obj: smtplib.SMTP
    if security == 'ssl':
        smtp_obj = smtplib.SMTP_SSL(host=email_settings.smtp_host,
                                    port=email_settings.smtp_port)
    else:
        smtp_obj = smtplib.SMTP(host=email_settings.smtp_host,
                                port=email_settings.smtp_port)

    if security == 'starttls':
        smtp_obj.starttls()

    if email_settings.use_auth:
        smtp_obj.login(user=email_settings.smtp_user,
                       password=email_settings.smtp_password)

    return smtp_obj


def send_test_email(email_settings: EmailSettings) -> None:
    validate_email_settings(email_settings)

    msg = email.message.EmailMessage()
    msg['From'] = email_settings.from_address
    msg['To'] = email_settings.to_address
    msg['Subject'] = 'Alert test email'
    msg['Date'] = email.utils.formatdate()
    msg['Message-ID'] = email.utils.make_msgid()

    body = "This is an email sent to test the alert email configuration."
    msg.set_content(body)

    smtp_obj = _get_smtp_object(email_settings)
    try:
        smtp_obj.send_message(msg)
    finally:
        smtp_obj.quit()


class AlertEmailManager:
    def __init__(self, preferences: Preferences):
        super().__init__()

        self.preferences = preferences

        self.update_preferences()
        self.email_settings: Optional[EmailSettings]
        self.last_sent: dict[str, datetime.datetime] = {}

        self.is_finished = threading.Event()
        self.alerts: collections.deque[tuple[AlertInfo, EmailCallback]] = \
            collections.deque()
        self.email_thread = threading.Thread(target=self._email_loop)

        # start
        self.email_thread.start()

    def update_preferences(self) -> None:
        if self.preferences.alert_email_enabled:
            try:
                self.email_settings = preferences_to_email_settings(
                    self.preferences)
                validate_email_settings(self.email_settings)
            except Exception:
                logger.exception("Invalid email settings")
                self.email_settings = None
        else:
            self.email_settings = None

    def _create_message(
            self,
            alert_info: AlertInfo,
            email_settings: EmailSettings) -> email.message.EmailMessage:

        if alert_info.display_name == alert_info.serial_number:
            name = alert_info.serial_number
        else:
            name = "{} ({})".format(alert_info.display_name,
                                    alert_info.serial_number)

        msg = email.message.EmailMessage()
        msg['From'] = email_settings.from_address
        msg['To'] = email_settings.to_address
        msg['Subject'] = '[{}] Alert'.format(name)
        msg['Date'] = email.utils.format_datetime(alert_info.dt)
        msg['Message-ID'] = email.utils.make_msgid()

        timestr = alert_info.dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        lines = [(f"{name} experienced an alert condition at {timestr}"
                  " with the following:"),
                 ""]

        for trigger, subchannel_name in alert_info.trigger_list:
            alert_type = trigger.limit_type.value
            s = f'{alert_type} alert triggered on "{subchannel_name}".'
            lines.append(s)

        body = "\n".join(lines)
        msg.set_content(body)

        return msg

    def _do_email(self, alert_info: AlertInfo,
                  callback: EmailCallback) -> None:
        if not self.email_settings:
            return  # email is disabled

        try:
            msg = self._create_message(alert_info, self.email_settings)
            smtp_obj = _get_smtp_object(self.email_settings)
            try:
                smtp_obj.send_message(msg)
            finally:
                smtp_obj.quit()

            callback(None)  # success
        except Exception as e:
            callback(e)  # failure

    def _email_loop(self) -> None:
        try:
            logger.debug("Email loop started")

            while True:
                if self.is_finished.is_set():
                    return

                # see if anything is ready for upload
                try:
                    alert_tuple, callback = self.alerts.popleft()
                except IndexError:
                    # short delay when empty; no need to max out CPU
                    time.sleep(0.1)
                    continue

                self._do_email(alert_tuple, callback)
        except Exception:
            logger.exception("Uncaught exception in email_loop")
            self.stop()

    def send_alerts(
            self, device_logger: DeviceLoggerAdapter, serial_number: str,
            display_name: str, trigger_list: list[tuple[Trigger, str]],
            callback: EmailCallback) -> None:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)

        last = self.last_sent.get(serial_number)
        if last is None or (dt - last) >= datetime.timedelta(minutes=10):
            alert_info = AlertInfo(
                serial_number=serial_number,
                display_name=display_name,
                trigger_list=trigger_list,
                dt=dt,
            )
            self.alerts.append((alert_info, callback))
            self.last_sent[serial_number] = dt
        else:
            device_logger.info("Alert email skipped. Email recently sent.")

    def stop(self) -> None:
        self.is_finished.set()

    def join(self) -> None:
        self.email_thread.join()
