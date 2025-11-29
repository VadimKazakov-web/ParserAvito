import logging
import time
import selenium.common
import urllib3
import re


class OpenUrl:

    def __init__(self, driver):
        self._url = None
        self._driver = driver
        self._data = []
        self._url_root = 'https://www.avito.ru'
        self._pattern_404 = re.compile(r'404')
        self._pattern_problem_ip = re.compile(r'Доступ ограничен')
        self._counter_timeout_exception = 3

    def open_url(self):
        counter = 3
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
                return

    def find_blocks(self):
        pass

    def collect_data(self, blocks):
        pass

    def check_title(self):
        while True:
            title = self._driver.title
            if self._pattern_problem_ip.search(title):
                print("page title: {}".format(title))
                time.sleep(3)
            elif self._pattern_404.search(title):
                return
            else:
                break

    @property
    def data(self):
        return self._data

    def start(self, url):
        self._data = []
        self._url = url
        while self._counter_timeout_exception:
            try:
                self.open_url()
                self.check_title()
                blocks = self.find_blocks()
                self.collect_data(blocks)
            except selenium.common.exceptions.TimeoutException:
                logging.info("\nTimeoutException in self.find_blocks()")
                self._counter_timeout_exception -= 1
            else:
                self.collect_data(blocks)
                break
        else:
            logging.info("\nTimeoutException,  bad connection")


