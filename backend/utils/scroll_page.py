# -*- coding: utf-8 -*-
import time
from seleniumwire.webdriver import Chrome
from typing import Generator


def scroll_page(driver: Chrome, height: int) -> Generator[None, None, None]:
    """
    Прокрутка страницы на заданную высоту
    :param driver: драйвер selenium
    :param height: высота прокрутки
    :return: Generator
    """
    step = 2
    while height > 0:
        driver.execute_script(f"window.scrollBy(0, {step});")
        height -= step
        time.sleep(0.01)
        yield
