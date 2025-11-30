import logging
import time
import selenium.common
import urllib3
import re
from parser_avito_manager import CheckTitleClass


class OpenUrl:

    def __init__(self, driver):
        self._url = None
        self._driver = driver
        self._data = None
        self._url_root = 'https://www.avito.ru'
        self._counter_timeout_exception = 3

    @property
    def data(self):
        return self._data

    def open_url(self):
        counter = self._counter_timeout_exception
        while counter:
            try:
                self._driver.get(self._url)
            except urllib3.exceptions.ReadTimeoutError:
                logging.info("\nReadTimeoutError in self.open_url()")
                counter -= 1
            except selenium.common.exceptions.TimeoutException:
                logging.info("\nTimeoutError in self.open_url()")
                counter -= 1
            else:
                break
        else:
            logging.info("\nTimeoutException,  bad connection")

    def find_blocks(self):
        pass

    def collect_data(self, blocks):
        pass

    def start(self, url):
        self._url = url
        counter = self._counter_timeout_exception
        while counter:
            self.open_url()
            check_title = CheckTitleClass()
            check_title.check_title(self._driver.title)
            try:
                blocks = self.find_blocks()
            except selenium.common.exceptions.TimeoutException:
                logging.info("\nTimeoutException in self.find_blocks()")
                counter -= 1
            else:
                self.collect_data(blocks)
                break
        else:
            logging.info("\nTimeoutException,  bad connection")


