import binascii
import io
import json
import logging
import lzma
import os
from typing import Any, Callable, Optional

import asphodel

from asphodel.device_info import DeviceInfo


BootloaderCallback = Callable[[int, int, str], None]


def get_default_file(device_info: DeviceInfo,
                     base_dir: Optional[str] = None) -> tuple[str, str]:
    if not base_dir:
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../"))

    try:
        import firmutil.repo_info
        boardname, boardrev = device_info.board_info
        repo = firmutil.repo_info.get_repo_from_board(boardname, boardrev)
    except ImportError:
        repo = None

    if not repo:
        repo = device_info.repo_name

    if not repo:
        # couldn't figure it out
        return ("", "")

    file_dir = os.path.abspath(
        os.path.join(base_dir, f"{repo}/firmware/build"))

    if not os.path.exists(file_dir):
        return ("", "")

    for file_name in os.listdir(file_dir):
        if os.path.splitext(file_name)[1] == ".firmware":
            return (file_dir, file_name)

    return ("", "")


def decode_firm_file(firm_file: str) -> dict[str, Any]:
    with lzma.LZMAFile(firm_file) as lzma_file:
        with io.TextIOWrapper(lzma_file) as f:
            return json.load(f)


def decode_firm_bytes(firm_bytes: bytes) -> dict[str, Any]:
    json_str = lzma.decompress(firm_bytes).decode()
    return json.loads(json_str)


def already_programmed(firm_data: dict[str, Any],
                       device_info: DeviceInfo) -> bool:
    if device_info.supports_bootloader:
        # don't assume anything if it's in the bootloader
        return False

    # make sure the data matches
    if firm_data.get('build_info') != device_info.build_info:
        return False
    if firm_data.get('build_date') != device_info.build_date:
        return False

    if firm_data.get('application', False) is not True:
        # firmware isn't for the application, abort
        return False

    if firm_data.get('bootloader', False) is not False:
        # firmware also contains the bootloader, abort
        return False

    # if we've made it to this point then the firmware contains the application
    # and only the application and it matches the build info strings already
    # present on the running application
    return True


def do_bootload_page(device: asphodel.AsphodelNativeDevice, done_bytes: int,
                     page_data: bytes, block_sizes: tuple[int, ...],
                     total_bytes: int, message: str,
                     callback: BootloaderCallback) -> None:
    index = 0
    remaining = len(page_data)
    while remaining > 0:
        block_size = max(x for x in block_sizes if x <= remaining)
        device.write_bootloader_code_block(page_data[index:index + block_size])
        index += block_size
        remaining -= block_size

        callback(done_bytes + index, total_bytes, message)


def do_bootload_pass(device: asphodel.AsphodelNativeDevice,
                     firm_data: dict[str, Any], block_sizes: tuple[int, ...],
                     verify_size: int, total_bytes: int,
                     callback: BootloaderCallback) -> None:
    done_bytes = 0

    for page_info in firm_data['data']:
        page_number = page_info[0]
        nonce = binascii.a2b_hex(page_info[1])
        page_data = binascii.a2b_hex(page_info[2])
        digest = binascii.a2b_hex(page_info[3])

        message = "Writing Page {}".format(page_number)
        callback(done_bytes, total_bytes, message)

        # see if the page needs to be written
        device.start_bootloader_page(page_number, nonce)
        try:
            device.verify_bootloader_page(digest)
            different = False
        except asphodel.AsphodelError as e:
            if e.args[1] == "ERROR_CODE_INVALID_DATA":
                different = True
            else:
                raise

        if different:
            device.start_bootloader_page(page_number, nonce)
            do_bootload_page(device, done_bytes, page_data, block_sizes,
                             total_bytes, message, callback)
            device.finish_bootloader_page(digest)

        done_bytes += len(page_data)

    for page_info in firm_data['data']:
        page_number = page_info[0]
        nonce = binascii.a2b_hex(page_info[1])
        digest = binascii.a2b_hex(page_info[3])

        message = "Verifying Page {}".format(page_number)
        callback(done_bytes, total_bytes, message)

        device.start_bootloader_page(page_number, nonce)
        device.verify_bootloader_page(digest)

        done_bytes += verify_size


def do_bootload(device: asphodel.AsphodelNativeDevice, serial_number: str,
                logger: logging.LoggerAdapter, firm_data: dict[str, Any],
                callback: BootloaderCallback) -> None:
    tries = 3
    block_sizes = None

    # figure out how many bytes need to be written
    write_bytes = sum(len(binascii.a2b_hex(p[2])) for p in firm_data['data'])

    # start the bootloader
    if not device.supports_bootloader_commands():
        callback(0, 0, "Switching to bootloader...")
        device.bootloader_jump()
        device.reconnect(bootloader=True, serial_number=serial_number)
        logger.info("Switched to bootloader")

    while True:
        try:
            if block_sizes is None:
                block_sizes = device.get_bootloader_block_sizes()

            # assume a page verify takes the same amount of time as writing
            #  the largest block size
            verify_size = max(block_sizes)
            verify_bytes = verify_size * len(firm_data['data'])

            total_bytes = write_bytes + verify_bytes

            do_bootload_pass(device, firm_data, block_sizes, verify_size,
                             total_bytes, callback)
        except asphodel.AsphodelError:
            tries -= 1
            if tries == 0:
                raise
            else:
                # connect to bootloader
                device.reconnect(bootloader=True, serial_number=serial_number)

                # try again
                continue
        break  # exit the loop

    build_info = firm_data.get('build_info')
    if build_info:
        logger.info("Firmware updated to %s", build_info)
    else:
        logger.info("Firmware updated")

    # start the application
    callback(0, 0, "Switching to main app...")
    device.bootloader_start_program()
    device.reconnect(application=True, serial_number=serial_number)
    logger.info("Switched back to main app")
