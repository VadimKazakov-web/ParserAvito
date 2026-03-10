# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import winreg
import logging
import platform
from pathlib import Path
from exceptions import PlatformError


def get_pyinstaller_work_dir(work_dir):
    command = "whoami"
    completed_process = subprocess.run(command, executable=None, capture_output=True, shell=True)
    if completed_process.returncode == 0:
        logging.info("_compile_repo: done")
        std_out = completed_process.stdout.decode(encoding="utf-8")
        comp, username = std_out.split("\\")
        username = username.strip()
        path = Path(get_drive_path()) / Path("Users") / Path(username) / Path(work_dir)
        return path
    else:
        logging.warning(completed_process.stderr.decode(encoding="utf-8"))


def get_drive_path():
    system_res = platform.system()
    if system_res == "Windows":
        drive = Path(os.getcwd()).drive
        drive += "\\"
        return Path(drive)
    else:
        raise PlatformError


def get_desktop_path():
    # Путь к ключу
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as key:
            value, reg_type = winreg.QueryValueEx(key, "Desktop")
            logging.info("Desktop path: {}".format(value))
    except FileNotFoundError:
        logging.warning("KEY not found in get_desktop_path\nKEY: Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    except PermissionError:
        logging.warning("PermissionError in get_desktop_path")
    else:
        return value
    finally:
        winreg.CloseKey(winreg.HKEY_CURRENT_USER)

