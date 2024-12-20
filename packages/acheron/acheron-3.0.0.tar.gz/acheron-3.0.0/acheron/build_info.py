import functools
import logging
import os
import sys
from typing import Optional

logger = logging.getLogger(__name__)


@functools.cache
def _load_values() -> Optional[tuple[str, str, str, str]]:
    is_frozen = getattr(sys, 'frozen', False)

    if is_frozen:
        # load the build_info.txt
        main_dir = os.path.dirname(sys.executable)
        build_info_filename = os.path.join(main_dir, "build_info.txt")
        try:
            with open(build_info_filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
                branch_name = lines[0].strip()
                commit_hash = lines[1].strip()
                build_key = lines[2].strip()
                build_date = lines[3].strip()
                return (branch_name, commit_hash, build_key, build_date)
        except Exception:
            logger.exception('Could not read build_info.txt')

    return None


def get_branch_name() -> Optional[str]:
    values = _load_values()
    if values:
        return values[0]
    else:
        return None


def get_commit_hash() -> Optional[str]:
    values = _load_values()
    if values:
        return values[1]
    else:
        return None


def get_build_key() -> Optional[str]:
    values = _load_values()
    if values:
        return values[2]
    else:
        return None


def get_build_date() -> Optional[str]:
    values = _load_values()
    if values:
        return values[3]
    else:
        return None
