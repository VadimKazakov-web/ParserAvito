# -*- coding: utf-8 -*-
import queue
import re
from objects import connector
import logging
import selenium.common
from exceptions import BreakWhile, BadInternetConnection, PushStopButton
from parser_avito_manager import CheckTitleMixin, TimeMeasurementMixin
from settings import TIMEOUT_EXCEPTIONS_COUNTER, TIMEOUT
import time


def check_chanel():
    """
    Проверяет очередь данных, в частности, не нажата ли кнопка "Stop"
    """
    try:
        data = connector.channel_for_variables.get(block=False)
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

    def __init__(self, driver, instance, links):
        TimeMeasurementMixin.time_measurement_start()
        self._driver = driver
        self._instance = instance
        self._links = links
        self._timeout_exceptions_counter = TIMEOUT_EXCEPTIONS_COUNTER
        self._timeout = TIMEOUT
        self._counter = 0
        self._pattern_timeout = re.compile(r'Timed out|timed out')

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
        for url in self._links:
            self._create_while(url)

    def _create_while(self, url):
        """
        Если возникновение ошибок таймаута больше разрешённых попыток self._timeout_exceptions_counter,
        выходим из цикла с ошибкой "плохого соединения" BadInternetConnection
        """
        timeout_exceptions_counter = self._timeout_exceptions_counter
        while timeout_exceptions_counter:
            try:
                self._main_block(url)
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

    def _main_block(self, url):
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
            self._instance.start(url)
            raise BreakWhile
