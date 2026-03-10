# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.window_root.build import window
import time
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
    _link_for_zip_archive = ""
    _icon_path = ""
    _prog_path = ""
    _headers = {
        "Accept": "application/json,text/html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36",
    }
    _repo = REPOSITORY
    _repo_name = Path(REPOSITORY).stem
    _repo_dir = _repo_name
    _archive_name = Path(f'{_repo_name}.zip')
    _archive_path = PYINSTALLER_WORK_DIR / _archive_name
    _unpack_archive = PYINSTALLER_WORK_DIR / Path("project-repo")

    @classmethod
    def check_update(cls, *args, **kwargs):
        tag = cls._request_new_tag()
        if not check_current_version_and_new_tag(tag, VERSION):
            text = f'доступна новая версия: {tag}'
            connector.update_version(text=text)
            connector.gen_install_event()
        else:
            text = f'нет новой версии'
            connector.update_version(text=text)

    @classmethod
    def update(cls, *args, **kwargs):
        delete_task(task=SCHTASKS_NAME)
        PYINSTALLER_WORK_DIR.mkdir(parents=True, exist_ok=True)
        url = extra_vision_var(cls._new_tag)
        cls._download_file(url)
        cls._unpack_zip_archive()
        cls._unpack_project_root = cls._search_project_dir()
        logging.info("cls._unpack_project_root: {}".format(cls._unpack_project_root))
        cls._icon_path = search_file(path=cls._unpack_project_root, suffix=".ico")
        cls._compile_repo()
        cls._prog_path = search_file(path=cls._unpack_project_root, suffix=".exe")
        logging.info("cls._prog_path: {}".format(cls._prog_path))
        try:
            cls._prog_path = reach_new_path(path=cls._prog_path, desktop=PYINSTALLER_WORK_DIR)
        except ManyExeFile:
            connector.update_info(text="много созданных экземпляров программы")
            return
        logging.info("cls._prog_path: {}".format(cls._prog_path))
        create_task_for_update(path=cls._prog_path, t_name=SCHTASKS_NAME)
        run_task_for_update(task=SCHTASKS_NAME)
        window.exit()

    @classmethod
    def _request_new_tag(cls):
        response = requests.get(url=cls._repo_tags, headers=cls._headers)
        st_code = response.status_code
        if st_code == 200:
            gen = cls._pattern_tags.finditer(response.text)
            match = next(gen)
            tag = match.group("tag")
            cls._new_tag = tag
            logging.info("new tag repository: {}".format(cls._new_tag))
            return tag
        else:
            logging.warning(f'_request_new_tag: response.status_code == {st_code}')

    @classmethod
    def _download_file(cls, url):
        time.sleep(1)
        response = requests.get(url, headers=cls._headers)
        if response.status_code == 200:
            cls._archive_path.write_bytes(response.content)

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
        command = r"pyinstaller --name {name}[{tag}] --distpath {path} --workpath {path} --specpath {path} --icon {icon_path} --onefile --noconsole {path_script}".format(
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
    def _compile_current_repo(cls):
        cls._unpack_project_root = Path(os.getcwd())
        cls._icon_path = Path(os.getcwd()) / Path("free-icon-web-crawler-11892629.ico")
        command = r"pyinstaller --name {name}({tag}) --distpath {path} --workpath {path} --specpath {path} --icon {icon_path} --onefile --noconsole {path_script}".format(
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
    def _search_project_dir(cls):
        for child in cls._unpack_archive.iterdir():
            if child.stem.startswith(cls._repo_name):
                return Path(child)
