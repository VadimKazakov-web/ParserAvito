# -*- coding: utf-8 -*-
import logging
import PyInstaller.__main__

from exceptions import ManyExeFile
from objects import connector
from tkinter_frontend.window_root.build import window
from settings import *
import subprocess
import requests
import re
import shutil
from update.utills.utills import (search_file,
                                  check_current_version_and_new_tag, extra_vision_var, reach_new_path,
                                  create_task_for_update, delete_task, run_task_for_update)


class Update:
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

    @classmethod
    def check_update(cls, *args, **kwargs):
        tag = cls._request_new_tag()
        if not check_current_version_and_new_tag(tag, VERSION):
            text = f'доступна новая версия: {tag}'
            cls._program_path = PYINSTALLER_WORK_DIR / Path(f'{cls._repo_name}[{tag}].exe')
            connector.update_version(text=text)
            connector.gen_install_event()
        else:
            text = f'нет новой версии'
            connector.update_version(text=text)

    @classmethod
    def update(cls, *args, **kwargs):
        delete_task(task=SCHTASKS_NAME)
        PYINSTALLER_WORK_DIR.mkdir(parents=True, exist_ok=True)
        cls._download_file(url=URL_S3_BUCKET, path_file=cls._program_path)
        logging.info("cls._program_path: {}".format(cls._program_path))
        try:
            cls._program_path = reach_new_path(path=cls._program_path, desktop=BASE_DIR.parent)
        except ManyExeFile:
            connector.update_info(text="много созданных экземпляров программы")
            return
        logging.info("cls._program_path: {}".format(cls._program_path))
        create_task_for_update(path=cls._program_path, t_name=SCHTASKS_NAME)
        run_task_for_update(task=SCHTASKS_NAME)
        window.exit()

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

    @classmethod
    def _download_file(cls, url: str, path_file: Path) -> None:
        response = requests.get(url, headers=cls._headers)
        if response.status_code == 200:
            path_file.write_bytes(response.content)

    def _get_repo(self):
        # Аргумент shell (по умолчанию False),
        # указывающий, следует ли использовать оболочку в качестве исполняемой программы.
        # Если shell равно True, рекомендуется передавать args в виде строки, а не последовательности.
        # Аргумент executable указывает на программу-заглушку, которую нужно запустить.
        # Он используется крайне редко. Когда shell=False, executable заменяет программу, указанную в args.
        # Однако исходные args по-прежнему передаются программе.
        completed_process = subprocess.run(f'git clone {REPOSITORY} {self._repo_dir}', executable=None,
                                           capture_output=True, shell=True)
        if completed_process.returncode == 0:
            logging.info("_get_repo: done")

    @classmethod
    def _unpack_zip_archive(cls):
        shutil.unpack_archive(filename=cls._archive_path, extract_dir=cls._unpack_archive, format="zip")

    @classmethod
    def _compile_repo(cls):
        logging.info("_compile_repo: start")
        command = "pyinstaller --name {name}[{tag}] --distpath {path} --workpath {path} --specpath {path} --icon {icon_path} --onefile --noconsole {path_script}".format(
            name=APP_NAME,
            tag=cls._new_tag,
            path=cls._unpack_project_root,
            path_script=cls._unpack_project_root / Path("main.py"),
            icon_path=cls._icon_path
        )
        completed_process = subprocess.run(command, executable=None, capture_output=True, shell=True)
        if completed_process.returncode == 0:
            logging.info("_compile_repo: done")
        else:
            logging.warning(completed_process.stderr.decode(encoding="utf-8"))

    @classmethod
    def _compile_repo_from_code(cls):
        logging.info("_compile_repo: start")
        command = "pyinstaller --name {name}[{tag}] --distpath {path} --workpath {path} --specpath {path} --icon {icon_path} --onefile --noconsole {path_script}".format(
            name=APP_NAME,
            tag=cls._new_tag,
            path=cls._unpack_project_root,
            path_script=cls._unpack_project_root / Path("main.py"),
            icon_path=cls._icon_path
        )
        command_list = command.split(" ")[1:]
        logging.info("command list: \n{}".format(command_list))
        PyInstaller.__main__.run(command_list)
        logging.info("_compile_repo: done")

    @classmethod
    def _test_pyinstaller(cls):
        logging.info("_test_pyinstaller: start")
        command = "python -m PyInstaller"
        completed_process = subprocess.run(command, executable=None, capture_output=True, shell=True)
        if completed_process.returncode == 0:
            logging.info(completed_process.stdout.decode(encoding="oem"))
            logging.info("_compile_repo: done")
        else:
            logging.warning(completed_process.stderr.decode(encoding="oem"))

    @classmethod
    def _search_project_dir(cls):
        for child in cls._unpack_archive.iterdir():
            if child.stem.startswith(cls._repo_name):
                return Path(child)
