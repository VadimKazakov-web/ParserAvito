# -*- coding: utf-8 -*-
import logging
from selenium.webdriver.chrome.options import ChromiumOptions as Options
from seleniumwire.webdriver import Chrome


def setup_options() -> Options:
    options = Options()
    # Запускайте в автономном режиме, то есть без пользовательского интерфейса
    # или сервера отображения
    # options.add_argument("--headless")
    # браузер останется открытым после завершения процесса,
    # пока драйверу не будет отправлена команда выхода
    options.add_experimental_option("detach", True)
    # Запускает браузер в полноэкранном режиме, независимо от предыдущих настроек
    options.add_argument("--start-maximized")
    # укажите позицию окна
    # options.add_argument("--window-position=500,100")
    # укажите начальный размер окна
    # options.add_argument("--window-size=800,1000")
    # Отключает песочницу для всех типов процессов, которые обычно находятся в изолированной программной среде.
    # Предназначено для использования в качестве переключателя на уровне браузера только в целях тестирования
    # options.add_argument("--no-sandbox")
    # Указывает временной интервал, в течение которого веб-страница
    # должна быть загружена в текущем контексте просмотра
    options.timeouts = {"pageLoad": 30000}
    # Selenium WebDriver позволяет использовать прокси-настройки
    # options.proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': 'http.proxy:1234'})
    options.page_load_strategy = 'eager'
    # options.page_load_strategy = 'none'
    options.browser_version = 'stable'
    return options


def create_driver() -> Chrome:
    """
    Создание драйвера для работы с браузером
    """
    options = setup_options()
    driver = Chrome(options=options)
    driver.implicitly_wait(30)
    return driver


class CreateDriverMixin:

    @classmethod
    def create_driver(cls):
        cls.driver = create_driver()
        return cls.driver
