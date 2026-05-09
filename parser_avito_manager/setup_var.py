# -*- coding: utf-8 -*-
import logging
import threading
from pathlib import Path
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.webdriver import WebDriver
from seleniumwire.webdriver import Chrome
from exceptions import PushExit
from objects import connector
from parser_avito_manager import PreparationLinksForPages
from settings import BASE_DIR, DATABASE_DIR, DATABASE
from selenium.webdriver.chrome.options import ChromiumOptions as Options


def preparation_links(url, pages):
    """
    Подготовка ссылок на страницы
    """
    prep_links_instance = PreparationLinksForPages(url=url, pages=pages)
    result = prep_links_instance.start()
    return result


def setup_options():
    """
    Создание драйвера для работы с браузером
    """
    options = Options()
    # Запускайте в автономном режиме, то есть без пользовательского интерфейса
    # или сервера отображения
    # options.add_argument("--headless")
    # браузер останется открытым после завершения процесса,
    # пока драйверу не будет отправлена команда выхода
    options.add_experimental_option("detach", True)
    # Запускает браузер в полноэкранном режиме, независимо от предыдущих настроек
    options.add_argument("--start-maximized")
    # Отключает песочницу для всех типов процессов, которые обычно находятся в изолированной программной среде.
    # Предназначено для использования в качестве переключателя на уровне браузера только в целях тестирования
    # options.add_argument("--no-sandbox")
    # Указывает временной интервал, в течение которого веб-страница
    # должна быть загружена в текущем контексте просмотра
    options.timeouts = {"pageLoad": 30000}
    # Selenium WebDriver позволяет использовать прокси-настройки
    # options.proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': 'http.proxy:1234'})
    options.page_load_strategy = 'eager'
    options.browser_version = 'stable'
    return options


def create_driver():
    options = setup_options()
    driver = Chrome(options=options)
    driver.implicitly_wait(30)
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
        logging.info("id thread: {}".format(threading.get_native_id()))
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
        self.driver = create_driver()
        data = get_data_from_interface()
        data = definition_data(data)
        self._setup_variables(data)
        self._initial_text()
        self._links_dict = preparation_links(self._url, self._pages)

