# -*- coding: utf-8 -*-
import logging
import re
import shutil
import subprocess
import datetime
import random
from pathlib import Path
from exceptions import ManyExeFile
import string


def random_str(num):
    result = "".join(random.choices(string.ascii_lowercase, k=num))
    return result


def rename_path(path: Path) -> Path:
    parent = path.parent
    stem = path.stem
    suffix = path.suffix
    # присоединение к имени файла случайной строки, для гарантирования уникальности имени,
    # если такое имя файла уже существует
    stem += f'_{random_str(7)}{suffix}'
    new_path = parent / stem
    return path.rename(new_path)


def check_current_version_and_new_ver(new_ver: str, curver: str) -> bool:
    """
    Проверить полученную строку о новой версии с текущей версией программы
    """
    if new_ver != curver:
        logging.info("A new version has been discovered")
        return False
    else:
        return True


def get_datetime():
    """
    Получение необходимых даты и времени для внесения в xml файл настройки для создания задачи через schtasks
    """
    delta = datetime.timedelta(minutes=2)
    result = datetime.datetime.now() + delta
    _time = result.time()
    date = result.date()
    time_str = _time.strftime("%H:%M:00")
    return str(date), str(time_str)


def run_command_subprocess(command):
    """
    Выполнение необходимой команды
    """
    logging.info("run command: \n{}".format(command))
    completed_process = subprocess.run(
        command, shell=True,
        capture_output=True)
    if completed_process.returncode != 0:
        # сработала только кодировка "oem"
        logging.warning(completed_process.stderr.decode(encoding="oem", errors="replace"))
    else:
        print(command, "complete")

