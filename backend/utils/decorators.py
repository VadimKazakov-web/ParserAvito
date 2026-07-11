# -*- coding: utf-8 -*-
import selenium.common
import logging


class ExceptElementDecorator:
    counter = 3
    result = None
    flag = False
    err_obj = None

    @classmethod
    def err_handler(cls, text):
        if not cls.flag:
            logging.warning(text)
            cls.flag = True
        cls.counter -= 1

    @classmethod
    def not_err_handler(cls):
        if cls.flag:
            logging.warning("ElementException - eliminated")

    @classmethod
    def raise_err(cls):
        raise cls.err_obj


def stale_element_decorator(func):
    def wrapper(*args, **kwargs):
        result = None
        while ExceptElementDecorator.counter:
            try:
                result = func(*args, **kwargs)
            except selenium.common.exceptions.StaleElementReferenceException as err:
                ExceptElementDecorator.err_obj = err
                text = str(err)[:200]
                ExceptElementDecorator.err_handler(text)
            except selenium.common.exceptions.NoSuchElementException as err:
                ExceptElementDecorator.err_obj = err
                text = str(err)[:200]
                ExceptElementDecorator.err_handler(text)
            else:
                ExceptElementDecorator.not_err_handler()
                break
        else:
            ExceptElementDecorator.raise_err()
        return result
    return wrapper

