# -*- coding: utf-8 -*-
import time


def scroll_page(driver, height):
    step = 2
    while height > 0:
        driver.execute_script(f"window.scrollBy(0, {step});")
        height -= step
        time.sleep(0.01)
        yield
