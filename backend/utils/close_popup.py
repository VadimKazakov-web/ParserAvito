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

    @classmethod
    def _find(cls, driver: Chrome) -> WebElement | None:
        try:
            block = driver.find_element(by=By.CSS_SELECTOR, value=cls._selector)
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

    @classmethod
    def close_popup(cls, driver: Chrome) -> None:
        from settings import DRIVER_IMPLICITLY_WAIT
        driver.implicitly_wait(2)
        block = cls._find(driver)
        if block:
            cls._click(block)
        driver.implicitly_wait(DRIVER_IMPLICITLY_WAIT)

