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

    def open_url(self):
        counter = 3
        while counter:
            try:
                self._driver.get(self._url)
            except urllib3.exceptions.ReadTimeoutError:
                logging.info("ReadTimeoutError")
                counter -= 1
            except selenium.common.exceptions.TimeoutException:
                logging.info("TimeoutError")
                counter -= 1
            else:
                return

    def find_blocks(self):
        pass

    def collect_data(self, blocks):
        pass

    @property
    def data(self):
        return self._data

    def start(self, url):
        self._data = []
        self._url = url
        self.open_url()
        while True:
            if self._pattern_problem_ip.search(self._driver.title):
                time.sleep(3)
            elif self._pattern_404.search(self._driver.title):
                return
            else:
                break
        blocks = self.find_blocks()
        self.collect_data(blocks)

