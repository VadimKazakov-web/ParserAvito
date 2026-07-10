# -*- coding: utf-8 -*-
import logging
import random
import re
from typing import Any
from settings import CATEGORY_DEFAULT

log = logging.getLogger(__name__)


class ValidationVarClass:
    """
    Класс проверяет необходимые переменные для парсера
    """
    file_name = 'result'
    pages = 2
    max_pages = 100
    _sub = "_"
    _pattern_for_check_url = re.compile(pattern=r'^https://www.avito.ru/.+')
    _pattern_space = re.compile(pattern=r'\s')
    _pattern_for_2_dot = re.compile(pattern=r':')
    _pattern_reverse_feature = re.compile(r'[\\]')
    _pattern_reverse_feature_2 = re.compile(r'[/]')
    _pattern_dangerous_func_1 = re.compile(r'exec')
    _pattern_dangerous_func_2 = re.compile(r'eval')
    _no_num = "no num"
    _limit_num = "limit num"

    @classmethod
    def _random_category(cls):
        category = random.choice(
            CATEGORY_DEFAULT
        )
        return category

    @classmethod
    def validation_url(cls, text: str) -> bool | str:
        if text == '':
            return cls._random_category()
        if cls._pattern_for_check_url.match(string=text):
            return text
        else:
            return False

    @classmethod
    def validation_file_name(cls, text: str) -> str:
        if text == '':
            return cls.file_name
        match = cls._pattern_space.sub(string=text, repl=cls._sub)
        match = cls._pattern_for_2_dot.sub(string=match, repl=cls._sub)
        match = cls._pattern_reverse_feature.sub(string=match, repl=cls._sub)
        match = cls._pattern_reverse_feature_2.sub(string=match, repl=cls._sub)
        match = cls._pattern_dangerous_func_1.sub(string=match, repl=cls._sub)
        match = cls._pattern_dangerous_func_2.sub(string=match, repl=cls._sub)
        return match

    @classmethod
    def validation_pages(cls, text: str) -> Any:
        try:
            num = int(text)
        except ValueError:
            return cls._no_num
        else:
            if num > cls.max_pages:
                return cls._limit_num
            elif num == 0:
                return 0
            else:
                return True
