# -*- coding: utf-8 -*-
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from seleniumwire.webdriver import Chrome


class CloseAuthPopupMixin:

    """
    Класс используется для нахождения всплывающего окна с предложением авторизоваться, и его закрытия
    """

    _selector = ".css-89rnpj"

    def __init__(self, driver: Chrome):
        self._driver = driver

    def _find(self, *args, **kwargs) -> WebElement | None:
        try:
            block = self._driver.find_element(by=By.CSS_SELECTOR, value=self._selector)
        except Exception as err:
            if re.search(r"no such element", str(err)):
                return None
            else:
                raise
        else:
            return block

    @classmethod
    def _click(cls, block: WebElement) -> None:
        block.click()

    def close_popup(self, *args, **kwargs) -> None:
        from settings import DRIVER_IMPLICITLY_WAIT
        self._driver.implicitly_wait(2)
        block = self._find()
        if block:
            self._click(block)
        self._driver.implicitly_wait(DRIVER_IMPLICITLY_WAIT)

