# -*- coding: utf-8 -*-
import re

import selenium.common
from selenium.webdriver.common.by import By


class CloseAuthPopupMixin:
    _class = ".css-89rnpj"

    def __init__(self, *args, **kwargs):
        self._driver = args[0]

    def _find(self):
        try:
            block = self._driver.find_element(by=By.CSS_SELECTOR, value=self._class)
        except Exception as err:
            if re.search(r"no such element", str(err)):
                return None
            else:
                raise err
        else:
            return block

    @classmethod
    def _click(cls, block):
        block.click()

    def close_popup(self, *args, **kwargs):
        self._driver.implicitly_wait(2)
        block = self._find()
        if block:
            self._click(block)
        self._driver.implicitly_wait(30)

