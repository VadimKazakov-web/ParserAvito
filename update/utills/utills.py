# -*- coding: utf-8 -*-
import logging
import re
import shutil
import subprocess
import datetime
import time
import random
from pathlib import Path
from exceptions import ManyExeFile
from objects import connector


def search_file(path: Path, suffix) -> Path:
    for child in path.iterdir():
        if child.suffix == suffix:
            return Path(child)


def random_str(num):
    text = [random.choice('qwertyuioplkhgfdsazxcvbnm') for _ in range(num)]
    result = ''.join(text)
    return result


def rename_path(path: Path) -> Path:
    parent = path.parent
    stem = path.stem
    suffix = path.suffix
    stem += f'_{random_str(7)}{suffix}'
    new_path = parent / stem
    return path.rename(new_path)


def reach_new_path(path: Path, desktop) -> Path:
    counter = 5
    while counter:
        try:
            logging.info("old path: {}".format(path))
            logging.info("new path: {}".format(desktop))
            new_path = shutil.move(src=path, dst=desktop)
        except shutil.Error as err:
            if re.search(r'already exists', err.args[0]):
                path = rename_path(path)
                counter -= 1
            else:
                raise err
        else:
            return Path(new_path)
    else:
        raise ManyExeFile


def check_current_version_and_new_tag(tag: str, curver: str) -> bool:
    if tag != curver:
        logging.info("A new version has been discovered")
        return False
    else:
        return True


def extra_vision_var(tag: str) -> str:
    """Не используется"""
    url = f'https://github.com/VadimKazakov-web/ParserAvito/archive/refs/tags/{tag}.zip'
    return url


def get_datetime():
    delta = datetime.timedelta(minutes=2)
    result = datetime.datetime.now() + delta
    _time = result.time()
    date = result.date()
    month = str(date.month)
    if len(month) < 2:
        month = "0" + month
    date_str = f"{date.year}-{month}-{date.day}"
    time_str = norm_hours_and_minute(str(_time.hour), str(_time.minute))
    return date_str, time_str


def norm_hours_and_minute(hour, minute):
    result = ""
    if len(hour) > 1:
        result += hour
    elif len(hour) == 1:
        result += f"0{hour}"
    result += ":"
    if len(minute) > 1:
        result += minute
    elif len(minute) == 1:
        result += f"0{minute}"
    result += ":00"
    return result


def run_command_subprocess(command):
    logging.info("run command: \n{}".format(command))
    completed_process = subprocess.run(
        command, shell=True,
        capture_output=True)
    if completed_process.returncode != 0:
        # сработала только кодировка "oem"
        logging.warning(completed_process.stderr.decode(encoding="oem", errors="replace"))
    else:
        logging.info("schtasks create: done")
        logging.info(completed_process.stdout.decode(encoding="oem", errors="replace"))

