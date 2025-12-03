import logging
import time
import selenium.common
import urllib3
import re
from parser_avito_manager import CheckTitleClass


class OpenUrl(CheckTitleClass):

    def __init__(self, driver, widget, data_for_progress):
        super().__init__(driver, widget, data_for_progress)
        self.widget = widget
        self.data_for_progress = data_for_progress
        self._url = None
        self._driver = driver
        self._data = None
        self._url_root = 'https://www.avito.ru'
        self._counter_timeout_exception = 3

    @property
    def data(self):
        return self._data

    def open_url(self, url):
        self._driver.get(url)
        # counter = self._counter_timeout_exception
        # while counter:
        #     try:
        #         self._driver.get(url)
        #     except urllib3.exceptions.ReadTimeoutError:
        #         logging.info("\nReadTimeoutError in self.open_url()")
        #         counter -= 1
        #     except selenium.common.exceptions.TimeoutException:
        #         logging.info("\nTimeoutError in self.open_url()")
        #         counter -= 1
        #     else:
        #         break
        # else:
        #     logging.info("\nTimeoutException,  bad connection")

    def find_blocks(self):
        pass

    def collect_data(self, blocks):
        pass

    def start(self, url):
        check_title = CheckTitleClass(self._driver, self.widget, self.data_for_progress)
        self.open_url(url)
        if check_title.check_title() == "404":
            return
        blocks = self.find_blocks()
        self.collect_data(blocks)

        # counter = self._counter_timeout_exception
        # check_title = CheckTitleClass(self._driver)
        # while counter:
        #     self.open_url(url)
        #     if check_title.check_title() == "404":
        #         return
        #     try:
        #         blocks = self.find_blocks()
        #     except selenium.common.exceptions.TimeoutException:
        #         logging.info("\nTimeoutException in self.find_blocks()")
        #         counter -= 1
        #     else:
        #         self.collect_data(blocks)
        #         break
        # else:
        #     logging.info("\nTimeoutException,  bad connection")


