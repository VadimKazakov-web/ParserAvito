# -*- coding: utf-8 -*-
import selenium.common
import logging


def stale_element_decorator(func):
    def wrapper(*args, **kwargs):
        counter = 4
        result = None
        flag = False
        while counter:
            try:
                result = func(*args, **kwargs)
            except selenium.common.exceptions.StaleElementReferenceException:
                logging.warning("StaleElementReferenceException in\nhow_to_search(self)")
                flag = True
                counter -= 1
            else:
                if flag:
                    logging.warning("StaleElementReferenceException - eliminated")
                break

        return result
    return wrapper

