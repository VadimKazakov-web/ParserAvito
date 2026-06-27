# -*- coding: utf-8 -*-
import logging
import re
import time
from seleniumwire.webdriver import Chrome
from backend.utils.timeout import TimeoutMixin


class CheckTitleMixin:

    """
    Класс для проверки заголовка страницы
    """

    _pattern_404 = re.compile(r'\b404\b')
    _pattern_problem_ip = re.compile(r'Доступ ограничен|доступ ограничен')
    _show_problem_ip_title = False

    @classmethod
    def check_title(cls, driver: Chrome) -> bool | None:
        while True:
            if cls._pattern_problem_ip.search(driver.title):
                if not cls._show_problem_ip_title:
                    logging.warning(driver.title)
                    cls._show_problem_ip_title = True
                    # добавить в диапазон таймаута по одной секунде в начало и в конец
                    TimeoutMixin.timeout_add_one()
                time.sleep(3)
            elif cls._pattern_404.search(driver.title):
                cls._show_problem_ip_title = False
                return None
            else:
                if cls._show_problem_ip_title:
                    logging.warning("капча решена")
                    cls._show_problem_ip_title = False
                return True
