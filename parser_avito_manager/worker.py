# -*- coding: utf-8 -*-
import queue
import re

from selenium.webdriver.common.by import By

from objects import connector
import logging
import selenium.common
from exceptions import BreakWhile, BadInternetConnection, PushStopButton, MaxPageError
from parser_avito_manager import CheckTitleMixin, TimeMeasurementMixin
from settings import TIMEOUT_EXCEPTIONS_COUNTER, TIMEOUT
import time


def check_chanel():
    """
    Проверяет очередь данных, в частности, не нажата ли кнопка "Stop"
    """
    try:
        data = connector.get_data_from_interface(block=False)
    except queue.Empty:
        return
    else:
        if data == "push_stop_button":
            raise PushStopButton


class Worker(CheckTitleMixin, TimeMeasurementMixin):
    """
    Класс использует экземпляры классов OpenPage и OpenAnnouncement.
    Обеспечивает открытие web-страниц с таймаутом, для обхода ограничения ip.
    Измеряет время работы программы.
    Ловит ошибки таймаутов и перезагружает страницу.
    """

    def __init__(self, driver, instance, start_method, **kwargs):
        TimeMeasurementMixin.time_measurement_start()
        self._driver = driver
        self._instance = instance
        self._links = kwargs.get("links")
        self._links_dict = kwargs.get("links_dict")
        self._start = start_method
        self._timeout_exceptions_counter = TIMEOUT_EXCEPTIONS_COUNTER
        self._timeout = TIMEOUT
        self._counter = 0
        self._counter_stale_element_exception = 3
        self._selected_page_selector = '.styles-module-pagination-enter_done-iw8uW'
        self._pattern_timeout = re.compile(r'Timed out|timed out')
        self._target_block_page = '.styles-module-pagination-enter_done-iw8uW'

    @classmethod
    def reset_time_start(cls):
        TimeMeasurementMixin.reset_time_start()

    def _driver_and_timeout(self, url):
        """
        Открытие web-страниц с таймаутом, для обхода ограничения ip.
        Проверка очереди данных.
        Измерение время работы программы.
        """
        check_chanel()
        self._driver.get(url)
        TimeMeasurementMixin.time_measurement_end()
        check_chanel()
        time.sleep(self._timeout / 2)
        check_chanel()
        time.sleep(self._timeout / 2)
        TimeMeasurementMixin.time_measurement_end()
        connector.update_time(text="время выполнения: {}".format(self.time_measurement_result()))

    def start(self):
        self._go_to_url()
        return self._instance

    def _go_to_url(self):
        """
        Обход ссылок
        """
        if self._links:
            for url in self._links:
                self._create_while(url=url)
        else:
            for page, url in self._links_dict.items():
                try:
                    self._create_while(page=page, url=url)
                except MaxPageError:
                    break

    def _create_while(self, *args, **kwargs):
        """
        Если возникновение ошибок таймаута больше разрешённых попыток self._timeout_exceptions_counter,
        выходим из цикла с ошибкой "плохого соединения" BadInternetConnection
        """
        page = kwargs.get("page")
        url = kwargs.get("url")
        timeout_exceptions_counter = self._timeout_exceptions_counter
        while timeout_exceptions_counter:
            try:
                self._main_block(page, url)
                timeout_exceptions_counter -= 1
            except BreakWhile:
                break
        else:
            connector.update_info(text="Плохое соединение с www.avito.ru")
            raise BadInternetConnection

    def _read_err_obj_timeout(self, err):
        """
        Отлов странной ошибки таймаута, которая не является экземпляром selenium.common.exceptions.TimeoutException
        """
        try:
            if self._pattern_timeout.search(err.args[0]):
                logging.warning("read with pattern: ")
                logging.warning("TimeoutException")
                connector.update_info(text="Плохое соединение, "
                                           "перезагружаю страницу")

            else:
                raise err
        except IndexError:
            raise err

    def _find_current_page(self):
        counter = self._counter_stale_element_exception
        current_page = None
        while counter:
            try:
                block = self._driver.find_element(by=By.CSS_SELECTOR, value=self._target_block_page)
                if block:
                    page_block = block.find_element(by=By.TAG_NAME, value='span').find_element(by=By.TAG_NAME, value='span')
                    current_page = page_block.get_attribute('innerHTML')
            except selenium.common.exceptions.StaleElementReferenceException:
                logging.warning("StaleElementReferenceException in\nfind_block(self)")
                counter -= 1
            else:
                return int(current_page)

    def _main_block(self, page, url):
        """
        Отлов типичных ошибок
        """
        try:
            self._driver_and_timeout(url)
            self.check_title(self._driver)
        except selenium.common.exceptions.TimeoutException:
            logging.warning("TimeoutException")
            connector.update_info(text="Плохое соединение, "
                                       "перезагружаю страницу")
        except PushStopButton:
            raise PushStopButton
        except Exception as err:
            self._read_err_obj_timeout(err)
        else:
            connector.update_info(text="Продолжаю открывать web-страницы")
            connector.update_title(text=self._driver.title)
            """
            Если нет ошибок, собрать данные со страницы
            """
            if page:
                current_page = self._find_current_page()
                if page > current_page:
                    logging.info("достигнуто максимальное колл-во страниц: {}".format(page))
                    raise MaxPageError
            self._start(url)
            raise BreakWhile
