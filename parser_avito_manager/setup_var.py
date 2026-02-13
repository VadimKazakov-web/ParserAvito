# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from selenium import webdriver
from exceptions import PushExit
from objects import connector
from parser_avito_manager import PreparationLinksForPages
from settings import BASE_DIR, DATABASE_DIR, DATABASE


def preparation_links(url, pages):
    """
    Подготовка ссылок на страницы
    """
    prep_links_instance = PreparationLinksForPages(url=url, pages=pages)
    prep_links_instance.start()
    return prep_links_instance.result_dict


def setup_options():
    """
    Создание драйвера для работы с браузером
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.timeouts = {"pageLoad": 30000}
    options.page_load_strategy = 'eager'
    options.browser_version = 'stable'
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(60)
    return driver


def get_data_from_interface():
    """
    Получение переменных из интерфейса
    """
    # блокирующий метод
    data = connector.get_data_from_interface()
    logging.info("data from tk: {}".format(data))
    return data


def definition_data(data):
    if isinstance(data, dict):
        return data
    elif data == "exit":
        """
        Нажатие кнопки "выход"
        """
        raise PushExit


class SetupVarMixin:

    def __init__(self):
        self.driver = None
        self._url = None
        self._pages = None
        self._file_name = None
        self._links_dict = None
        self._base_dir = BASE_DIR

    def _setup_variables(self, data):
        """
        Установка переменных, полученных из интерфейса tkinter
        """
        self._url = data.get("link")
        filename = data.get("filename")
        self._file_name = self._base_dir / Path(filename)
        self._pages = int(data.get("count_pages"))
        self._default_filename = data.get("default_filename")

    def _initial_text(self):
        """
        Начальные сообщения с какой-то информацией
        """
        logging.info("")
        logging.info("-" * 40)
        logging.info("start parser")
        logging.info("base dir: {}".format(BASE_DIR))
        logging.info("filename: {}".format(self._file_name))
        logging.info("database dir: {}".format(DATABASE_DIR))
        logging.info("database: {}".format(DATABASE))

    def setup_var(self):
        self.driver = setup_options()
        data = get_data_from_interface()
        try:
            data = definition_data(data)
            self._setup_variables(data)
        except PushExit:
            self.driver.quit()
            raise PushExit
        else:
            self._initial_text()
            self._links_dict = preparation_links(self._url, self._pages)

