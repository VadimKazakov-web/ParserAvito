# -*- coding: utf-8 -*-
import logging
import shutil
from objects import connector
from settings import *
import requests
import re
from tkinter_frontend.window_root.build import window
from update.utills.utills import (check_current_version_and_new_tag, get_datetime, rename_path, run_command_subprocess)
from utills.utils import get_version_prog


class Update:
    PYINSTALLER_WORK_DIR.mkdir(exist_ok=True)
    _pattern_tags = re.compile(r'href="/VadimKazakov-web/ParserAvito/releases/tag/(?P<tag>.+?)"')
    _repo_tags = REPOSITORY_TAGS
    _unpack_project_root = ""
    _new_tag = ""
    _headers = {
        "Accept": "application/json,text/html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36",
    }
    _repo = REPOSITORY
    _repo_name = Path(REPOSITORY).stem
    _repo_dir = _repo_name

    _program_path = None
    _xml_path = PYINSTALLER_WORK_DIR / Path("parser.xml")
    _version_prog_path = PYINSTALLER_WORK_DIR / Path("version.py")

    @classmethod
    def check_update(cls, *args, **kwargs):
        tag = cls._request_new_tag()
        if tag:
            if not check_current_version_and_new_tag(tag, VERSION):
                text = f'доступна новая версия: {tag}'
                cls._program_path = PYINSTALLER_WORK_DIR / Path(f'{cls._repo_name}[{tag}].exe')
                connector.update_version(text=text)
                connector.gen_install_event()
            else:
                text = 'нет новой версии'
                connector.update_version(text=text)

    @classmethod
    def update(cls, *args, **kwargs):
        command_delete_task = f"schtasks -delete -tn {SCHTASKS_NAME} -f"
        run_command_subprocess(command_delete_task)
        cls._download_file(url=URL_S3_BUCKET_PROG, path_file=cls._program_path)
        cls._download_file(url=URL_S3_BUCKET_XML, path_file=cls._xml_path)
        logging.info("cls._program_path: {}".format(cls._program_path))
        try:
            cls._program_path = shutil.move(src=cls._program_path, dst=BASE_DIR.parent)
        except shutil.Error as err:
            logging.info(err)
            if re.search(r'already exists', err.args[0]):
                cls._program_path = rename_path(cls._program_path)
                cls._program_path = shutil.move(src=cls._program_path, dst=BASE_DIR.parent)
        logging.info("cls._program_path: {}".format(cls._program_path))
        cls._create_xml_settings()
        command_create_task = "schtasks /create /tn {name} /xml {path}".format(name=SCHTASKS_NAME, path=cls._xml_path)
        run_command_subprocess(command_create_task)
        command_run_task = f"schtasks /run /tn {SCHTASKS_NAME}"
        run_command_subprocess(command_run_task)
        window.exit()

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
    def _request_new_tag(cls):
        try:
            response = requests.get(url=cls._repo_tags, headers=cls._headers)
        except requests.exceptions.ProxyError:
            logging.info("the client has a proxy enabled")
            connector.update_info(text="отключите прокси сервер или VPN")
            return
        st_code = response.status_code
        if st_code == 200:
            gen = cls._pattern_tags.finditer(response.text)
            match = next(gen)
            tag = match.group("tag")
            cls._new_tag = tag
            logging.info("last tag repository: {}".format(cls._new_tag))
            return tag
        else:
            logging.warning(f'_request_new_tag: response.status_code == {st_code}')
            cls._download_file(URL_S3_BUCKET_VERSION_PROG, cls._version_prog_path)
            ver = get_version_prog(cls._version_prog_path)
            return ver

    @classmethod
    def _download_file(cls, url: str, path_file: Path) -> None:
        response = requests.get(url, headers=cls._headers)
        if response.status_code == 200:
            logging.info("write in {}".format(path_file))
            path_file.write_bytes(response.content)
        else:
            logging.info("status code in _download_file: {}".format(response.status_code))
