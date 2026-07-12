# -*- coding: utf-8 -*-
import selenium.common
import logging


class FindElementDecorator:
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

    @classmethod
    def find_element_decorator(cls):
        def _decorator(func):
            def _wrapper(*args, **kwargs):
                result = None
                while cls.counter:
                    try:
                        result = func(*args, **kwargs)
                    except selenium.common.exceptions.StaleElementReferenceException as err:
                        cls.err_obj = err
                        text = str(err)[:200]
                        cls.err_handler(text)
                    except selenium.common.exceptions.NoSuchElementException as err:
                        cls.err_obj = err
                        text = str(err)[:200]
                        cls.err_handler(text)
                    else:
                        cls.not_err_handler()
                        break
                else:
                    cls.raise_err()
                return result

            return _wrapper
        return _decorator
