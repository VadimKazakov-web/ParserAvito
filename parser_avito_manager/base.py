# -*- coding: utf-8 -*-
import logging


class OpenUrl:
    """
    Родительский класс для OpenPage и OpenAnnouncement
    """

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

    def _find_blocks(self):
        pass

    def _collect_data(self, blocks):
        pass

    def start(self, url):
        self._url = url
        blocks = self._find_blocks()
        logging.info("blocks in OpenUrl: {}".format(blocks))
        if blocks:
            data = self._collect_data(blocks)
            logging.info("data in OpenUrl: {}".format(data))
            if data:
                return data
