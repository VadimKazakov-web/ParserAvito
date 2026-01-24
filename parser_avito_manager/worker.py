# -*- coding: utf-8 -*-
import queue
from settings import TOP_ANNOUNCEMENT
from objects import connector
import logging
import selenium.common
from exceptions import BreakWhile, BadInternetConnection, PushStopButton
from parser_avito_manager import CheckTitleMixin, TimeMeasurementMixin
from settings import TIMEOUT_EXCEPTIONS_COUNTER, TIMEOUT
import time


def check_chanel():
    try:
        data = connector.channel_for_variables.get(block=False)
    except queue.Empty:
        return
    else:
        if data == "push_stop_button":
            raise PushStopButton


class Worker(CheckTitleMixin, TimeMeasurementMixin):

    def __init__(self, driver, instance, links):
        TimeMeasurementMixin.time_measurement_start()
        self._driver = driver
        self._instance = instance
        self._links = links
        self._timeout_exceptions_counter = TIMEOUT_EXCEPTIONS_COUNTER
        self._timeout = TIMEOUT
        self._counter = 0
        self.total_data = None

    @classmethod
    def reset_time_start(cls):
        TimeMeasurementMixin.reset_time_start()

    def _driver_and_timeout(self, url):
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
        for url in self._links:
            self._create_while(url)

    def _create_while(self, url):
        timeout_exceptions_counter = self._timeout_exceptions_counter
        while timeout_exceptions_counter:
            try:
                self._main_block(url)
            except BreakWhile:
                break
        else:
            connector.update_info(text="Плохое соединение с www.avito.ru")
            raise BadInternetConnection

    def _main_block(self, url):
        try:
            self._driver_and_timeout(url)
            self.check_title(self._driver)
        except selenium.common.exceptions.TimeoutException:
            logging.warning("TimeoutException")
            connector.update_info(text="Плохое соединение, "
                                       "перезагружаю страницу,\n"
                                       "осталось попыток: {}"
                                  .format(self._timeout_exceptions_counter))
            self._timeout_exceptions_counter -= 1

        else:
            connector.update_info(text="Продолжаю открывать web-страницы")
            connector.update_title(text=self._driver.title)
            self._instance.start(url)
            raise BreakWhile
