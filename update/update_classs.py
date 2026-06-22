# -*- coding: utf-8 -*-
import logging
import shutil
from settings import *
import requests
import re
from tkinter_frontend.events import Events
from backend import connector
from update.utills.utills import (check_current_version_and_new_ver, get_datetime, rename_path, run_command_subprocess)
from utills.utils import get_version_prog
from backend.utils.utils import get_desktop_path


class Update:
    """
    Класс служит для проверки новой версии программы, загрузки программы во временную папку, перемещения её на рабочий стол,
    и дальнейший запуск
    """
    _repo_name = Path(REPOSITORY).stem
    _program_path = None
    _xml_path = APP_TEMPORARY / Path("parser.xml")
    _version_prog_path = APP_TEMPORARY / Path("version.py")

    @classmethod
    def check_update(cls, *args, **kwargs):
        from tkinter_frontend.utils import create_install_prog_btn
        from tkinter_frontend.window_root.frame_2.update_block.build import label_instance
        cls._download_file(URL_S3_BUCKET_VERSION_PROG, cls._version_prog_path)
        _version = get_version_prog(cls._version_prog_path)
        if _version:
            if not check_current_version_and_new_ver(_version, VERSION):
                label_instance["text"] = f'доступна новая версия: {_version}'
                cls._program_path = APP_TEMPORARY / Path(f'{cls._repo_name}[{_version}].exe')
                create_install_prog_btn()
            else:
                label_instance["text"] = 'нет новой версии'

    @classmethod
    def update(cls, *args, **kwargs):
        from update.update_thread import UpdateProgThread
        for _ in cls._update_gen():
            UpdateProgThread.update_plug(num=3)

    @classmethod
    def _update_gen(cls):
        cls._download_file(url=URL_S3_BUCKET_PROG, path_file=cls._program_path)
        yield
        cls._download_file(url=URL_S3_BUCKET_XML, path_file=cls._xml_path)
        yield
        print("cls._program_path: {}".format(cls._program_path))
        try:
            cls._program_path = shutil.move(src=cls._program_path, dst=get_desktop_path())
        except shutil.Error as err:
            print(err)
            if re.search(r'already exists', err.args[0]):
                cls._program_path = rename_path(cls._program_path)
                cls._program_path = shutil.move(src=cls._program_path, dst=get_desktop_path())
        yield
        print("cls._program_path: {}".format(cls._program_path))
        cls._create_xml_settings()
        command_create_task = "schtasks /create /tn {name} /xml {path}".format(name=SCHTASKS_NAME, path=cls._xml_path)
        run_command_subprocess(command_create_task)
        yield
        connector.put(Events.exit_after_update_event)
        yield

    @classmethod
    def _create_xml_settings(cls):
        xml_string = cls._xml_path.read_text(encoding="utf-16")
        date, _time = get_datetime()
        xml_string = xml_string.replace("{task}", SCHTASKS_NAME)
        xml_string = xml_string.replace("{date}", date)
        xml_string = xml_string.replace("{time}", _time)
        xml_string = xml_string.replace("{program_path}", str(cls._program_path))
        cls._xml_path.write_text(xml_string, encoding="utf-16")
    
    @classmethod
    def _download_file(cls, url: str, path_file: Path) -> None:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info("write in {}".format(path_file))
            path_file.write_bytes(response.content)
        else:
            logging.info("status code in _download_file: {}".format(response.status_code))
