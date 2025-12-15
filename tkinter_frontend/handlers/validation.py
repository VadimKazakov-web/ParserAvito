# -*- coding: utf-8 -*-
import logging
import re
from typing import Any

log = logging.getLogger(__name__)


class ValidationVarClass:
    """
    Класс проверяет необходимые переменные для парсера
    """
    url = 'https://www.avito.ru/moskva/avtomobili?radius=0&searchRadius=0'
    file_name = 'result.html'
    pages = 2
    max_pages = 25
    pattern_for_check_url = re.compile(pattern='^https://www.avito.ru/.+')
    pattern_for_check_file_name = re.compile(pattern='\s')
    pattern_for_2_dot = re.compile(pattern=':')

    @classmethod
    def validation_url(cls, text: str) -> bool | str:
        if ValidationVarClass.pattern_for_check_url.match(string=text):
            return text
        else:
            return False

    @classmethod
    def validation_file_name(cls, text: str) -> str:
        if text == '':
            return cls.file_name
        match = ValidationVarClass.pattern_for_check_file_name.sub(string=text, repl="_")
        match = ValidationVarClass.pattern_for_2_dot.sub(string=match, repl="_")
        return match + ".html"

    @classmethod
    def validation_pages(cls, text: str) -> Any:
        try:
            num = int(text)
        except ValueError:
            return 'ValueError'
        else:
            if num > cls.max_pages:
                return 'Limit'
            elif num == 0:
                return 0
            else:
                return True
