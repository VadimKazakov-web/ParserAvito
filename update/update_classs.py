# -*- coding: utf-8 -*-
import logging
import time
from objects import connector
from settings import *
import subprocess
import shutil
import requests
import re

FORMAT = '[%(asctime)s] %(message)s'
formatter = logging.Formatter(FORMAT)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.setLevel(logging.INFO)
logging.root.handlers.clear()
logging.root.addHandler(handler)


class Update:

    def __init__(self):
        self._repo = REPOSITORY
        self._repo_name = Path(REPOSITORY).stem
        self._repo_dir = self._repo_name
        self._repo_tags = REPOSITORY_TAGS
        self._pattern_tags = re.compile(r'href="/VadimKazakov-web/ParserAvito/releases/tag/(?P<tag>.+?)"')
        self._archive_name = Path(f'{self._repo_name}.zip')

        self._archive_path = BASE_DIR / self._archive_name
        self._unpack_project = BASE_DIR / Path("project-repo")

        self._unpack_project_root = ""
        self._new_tag = ""
        self._link_for_zip_archive = ""
        self._icon_path = ""
        self._prog_path = ""
        self._headers = {
            "Accept": "application/json,text/html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36",
        }

    def check_update(self, *args, **kwargs):
        tag = self._request_new_tag()
        if not self._check_current_version_and_new_tag(tag, VERSION):
            text = f'доступна новая версия \n{tag}'
            connector.update_version(text=text)
            connector.gen_install_event()
        else:
            text = f'нет новых версий'
            connector.update_version(text=text)

    def start(self):
        tag = self._request_new_tag()
        if not self._check_current_version_and_new_tag(tag, VERSION):
            url = self._extra_vision_var(tag)
            self._download_file(url)
            self._unpack_zip_archive()
            self._search_project_dir()
            self._icon_path = self._search_file(path=self._unpack_project_root, suffix=".ico")
            self._compile_repo()
            self._prog_path = self._search_file(path=self._unpack_project_root, suffix=".exe")
            logging.info(self._prog_path)

    @staticmethod
    def _check_current_version_and_new_tag(tag, curver):
        if tag != curver:
            logging.info("A new version has been discovered")
            return False
        else:
            return True

    @staticmethod
    def _extra_vision_var(tag):
        url = f'https://github.com/VadimKazakov-web/ParserAvito/archive/refs/tags/{tag}.zip'
        return url

    def _request_new_tag(self):
        response = requests.get(url=self._repo_tags, headers=self._headers)
        st_code = response.status_code
        if st_code == 200:
            gen = self._pattern_tags.finditer(response.text)
            match = next(gen)
            tag = match.group("tag")
            self._new_tag = tag
            logging.info("new tag repository: {}".format(self._new_tag))
            return tag
        else:
            logging.warning(f'_request_new_tag: response.status_code == {st_code}')

    def _download_file(self, url):
        time.sleep(1)
        response = requests.get(url, headers=self._headers)
        if response.status_code == 200:
            self._archive_path.write_bytes(response.content)

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

    def _unpack_zip_archive(self):
        shutil.unpack_archive(filename=self._archive_path, extract_dir=self._unpack_project, format="zip")

    def _compile_repo(self):
        completed_process = subprocess.run(f'pyinstaller --name {APP_NAME}({self._new_tag}) '
                                           f'--distpath {self._unpack_project_root} '
                                           f'--workpath {self._unpack_project_root} '
                                           f'--specpath {self._unpack_project_root} '
                                           f'--icon {self._icon_path} '
                                           f'--onefile --noconsole {self._unpack_project_root}/main.py',
                                           executable=None, capture_output=True,
                                           shell=True)
        if completed_process.returncode == 0:
            logging.info("_compile_repo: done")
        else:
            logging.warning(completed_process.stderr.decode(encoding="utf-8"))

    @staticmethod
    def _search_file(path, suffix):
        for child in Path(path).iterdir():
            if child.suffix == suffix:
                return child

    def _search_project_dir(self):
        for child in self._unpack_project.iterdir():
            if child.stem.startswith(self._repo_name):
                self._unpack_project_root = child
                break


# u = Update()
# u.start()
# p = Path(REPOSITORY)
# print(p.stem)
