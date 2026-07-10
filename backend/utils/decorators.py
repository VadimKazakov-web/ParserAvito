# -*- coding: utf-8 -*-
import re
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
                logging.warning("ElementReferenceException in\nhow_to_search(self)")
                flag = True
                counter -= 1
            except Exception as err:
                if re.search(r"no such element", str(err)):
                    logging.warning("Message: no such element: Unable to locate element in"
                                    "\nstale_element_decorator(self)")
                    flag = True
                    counter -= 1
            else:
                if flag:
                    logging.warning("ElementReferenceException - eliminated")
                break

        return result
    return wrapper

