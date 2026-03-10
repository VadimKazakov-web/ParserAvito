# -*- coding: utf-8 -*-
import logging
import re
import shutil
import subprocess
import datetime
from pathlib import Path
from exceptions import ManyExeFile
from objects import connector


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
    delta = datetime.timedelta(minutes=2)
    result = datetime.datetime.now() + delta
    time_str = norm_hours_and_minute(str(result.time().hour), str(result.time().minute))
    return time_str


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
    return result


def create_task_for_update(path, t_name):
    logging.info("path to task for schtasks: {}".format(path))
    time_for_command = get_time_for_command()
    command = (f'schtasks /create /tn {t_name} /tr {path}'
               f' /sc once /st {time_for_command}')
    logging.info("schtasks command: \n{}".format(command))
    completed_process = subprocess.run(
        command, shell=True,
        capture_output=True)
    if completed_process.returncode != 0:
        # сработала только кодировка "oem"
        logging.warning(completed_process.stderr.decode(encoding="oem", errors="replace"))
    else:
        logging.info("schtasks create: done")
        logging.info(completed_process.stdout.decode(encoding="oem", errors="replace"))


def run_task_for_update(task):
    command = f"schtasks /run /tn {task}"
    logging.info("schtasks command: \n{}".format(command))
    completed_process = subprocess.run(
        command, shell=True,
        capture_output=True)
    if completed_process.returncode != 0:
        # сработала только кодировка "oem"
        logging.warning(completed_process.stderr.decode(encoding="oem", errors="replace"))
    else:
        logging.info("schtasks create: done")
        logging.info(completed_process.stdout.decode(encoding="oem", errors="replace"))


def delete_task(task):
    command = f"schtasks -delete -tn {task} -f"
    logging.info("schtasks command: \n{}".format(command))
    completed_process = subprocess.run(
        command, shell=True,
        capture_output=True)
    if completed_process.returncode != 0:
        # сработала только кодировка "oem"
        logging.warning(completed_process.stderr.decode(encoding="oem", errors="replace"))
    else:
        logging.info(completed_process.stdout.decode(encoding="oem", errors="replace"))


class ControlPyinstallerWorkDir:

    _rm_dir = False

    @classmethod
    def control_pyinstaller_work_dir(cls, path, desktop):
        if path.exists() and not cls._rm_dir:
            prog_path = search_file(path=path, suffix=".exe")
            try:
                new_prog_path = reach_new_path(path=prog_path, desktop=desktop)
            except ManyExeFile:
                connector.update_info(text="много созданных экземпляров программы")
                return
            else:
                logging.info("the program has been moved: \n{}".format(new_prog_path))
            shutil.rmtree(path)
            logging.info("rm directory: \n{}".format(path))
            cls._rm_dir = True
