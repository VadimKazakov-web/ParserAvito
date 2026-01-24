# -*- coding: utf-8 -*-


class OpenUrl:

    def __init__(self, driver):
        self._driver = driver
        self._data = None
        self._url_root = 'https://www.avito.ru'
        self._url = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, list):
            self._data = value
        else:
            raise TypeError('data must be a list')

    def find_blocks(self):
        pass

    def _collect_data(self, blocks):
        pass

    def start(self, url):
        self._url = url
        blocks = self.find_blocks()
        if blocks:
            data = self.collect_data(blocks)
            return data
