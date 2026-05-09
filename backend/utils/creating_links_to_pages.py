# -*- coding: utf-8 -*-
import re
from typing import Generator


def check_url(url):
    match = re.search(r'[?]', url)
    if match:
        return url
    else:
        return url + '?'


class CreatingLinks:

    """
    Класс из базового url создаёт ссылки на страницы
    """

    def __init__(self, url: str, pages: int):
        self._url = url
        self._pages = pages

    def _create_result(self, url: str) -> Generator[str, None, None]:
        count = 1
        while count <= self._pages:
            yield url + f'&p={count}'
            count += 1

    def __call__(self, *args, **kwargs) -> Generator[str, None, None]:
        url = check_url(self._url)
        gen = self._create_result(url)
        for elem in gen:
            yield elem
