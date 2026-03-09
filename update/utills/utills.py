# -*- coding: utf-8 -*-
import logging
import re
import shutil
import subprocess
import time
import datetime
from pathlib import Path
from exceptions import ManyExeFile


def search_file(path: Path, suffix) -> Path:
    for child in path.iterdir():
        if child.suffix == suffix:
            return Path(child)


def rename_path(path: Path) -> Path:
    parent = path.parent
    stem = path.stem
    suffix = path.suffix
    stem += f'_{suffix}'
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
    url = f'https://github.com/VadimKazakov-web/ParserAvito/archive/refs/tags/{tag}.zip'
    return url


def get_time_for_command():
    delta = datetime.timedelta(minutes=1)
    delta_sec = datetime.timedelta(seconds=45)
    while True:
        if datetime.datetime.now().second > delta_sec.seconds:
            result = datetime.datetime.now() + delta
            hour = norm_hours(str(result.time().hour))
            minute = str(result.time().minute)
            print("task begin ", result.time())
            return {
                "hour": hour,
                "minute": minute,
            }
        else:
            time.sleep(2)
            print(datetime.datetime.now().time())


def norm_hours(hour):
    if len(hour) > 1:
        return hour
    elif len(hour) == 1:
        return f"0{hour}"


def create_task_for_update(path, t_name):
    new_path = str(path).replace(" ", "^ ")
    logging.info("path to task for schtasks: {}".format(new_path))
    time_for_command = get_time_for_command()
    command = (f'schtasks /create /tn {t_name} /tr {new_path}'
               f' /sc once /st {time_for_command.get("hour")}:{time_for_command.get("minute")}')
    logging.info("schtasks command: \n{}".format(command))
    completed_process = subprocess.run(
        command, shell=True,
        capture_output=True)
    if completed_process.returncode != 0:
        # сработала только кодировка "oem"
        logging.warning(completed_process.stderr.decode(encoding="oem", errors="replace"))
    else:
        logging.info("schtasks create: done")
