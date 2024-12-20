from typing import Optional

import asphodel


def find_and_open_tcp_device(
        serial_number: str,
        location: str) -> Optional[asphodel.AsphodelNativeDevice]:
    devices = asphodel.find_tcp_devices()
    for device in devices:
        device_location_string = device.get_location_string()
        if device_location_string == location:
            adv = device.tcp_get_advertisement()
            if adv.serial_number == serial_number:
                device.open()
                return device
    return None


def find_and_open_usb_device(
        location: str) -> Optional[asphodel.AsphodelNativeDevice]:
    devices = asphodel.find_usb_devices()
    for device in devices:
        device_location_string = device.get_location_string()
        if device_location_string == location:
            device.open()
            return device
    return None


def connect_and_open_tcp_device(host: str, port: int, timeout: int,
                                serial: str) -> asphodel.AsphodelNativeDevice:
    device = asphodel.create_tcp_device(host, port, timeout, serial)
    device.open()
    return device


def explode(device: asphodel.AsphodelNativeDevice) -> None:
    raise Exception("Explosion")
