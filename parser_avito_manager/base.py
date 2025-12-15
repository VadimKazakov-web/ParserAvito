# -*- coding: utf-8 -*-


class OpenUrl:

    def __init__(self, driver):
        self._driver = driver
        self._data = None
        self._url_root = 'https://www.avito.ru'

    @property
    def data(self):
        return self._data

    def find_blocks(self):
        pass

    def collect_data(self, blocks):
        pass

    def start(self):
        blocks = self.find_blocks()
        if blocks:
            self.collect_data(blocks)
