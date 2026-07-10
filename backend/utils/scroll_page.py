# -*- coding: utf-8 -*-
import asyncio
import time
from seleniumwire.webdriver import Chrome


async def scroll_page(driver: Chrome, height: int) -> None:
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
        await asyncio.sleep(0)
