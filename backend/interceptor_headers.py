# -*- coding: utf-8 -*-
import re
from seleniumwire.request import Request, Response


class InterceptorHeaders:

    """
    Класс актуализирует cookies в запросах, используются возможности seleniumwire.
    https://github.com/wkeeling/selenium-wire#:~:text=Selenium%20Wire-,Selenium%20Wire,-extends%20Selenium%27s%20Python
    """

    # словарь предварительно заполнен, чтобы избежать проверок на True в каждом запросе
    cookie_dict = {
        "foo": "bar",
    }
    referer = 'https://www.avito.ru'

    # cSyncDp104v3=1776189919; expires=Tue, 28-Apr-26 18:05:19 GMT; path=/; Secure; SameSite=None; domain=.acint.net
    # Acint.net — это интернет-счётчик, который предоставляет инструменты для сбора,
    # обработки и анализа данных о посетителях онлайн-ресурсов

    @classmethod
    def request_interceptor(cls, request: Request) -> None:

        del request.headers['accept']
        request.headers['accept'] = ('text/html,application/xhtml+xml,application/xml;q=0.9,'
                                     'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;'
                                     'v=b3;q=0.7')

        del request.headers['sec-ch-ua']
        request.headers['sec-ch-ua'] = '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"'

        del request.headers["sec-ch-ua-platform"]
        request.headers["sec-ch-ua-platform"] = '"Windows"'

        del request.headers["sec-fetch-site"]
        request.headers["sec-fetch-site"] = "same-origin"

        del request.headers["upgrade-insecure-requests"]
        request.headers["upgrade-insecure-requests"] = "1"

        del request.headers['accept-encoding']
        request.headers['accept-encoding'] = 'gzip, deflate, br, zstd'

        del request.headers['accept-language']
        request.headers['accept-language'] = 'ru,en;q=0.9'

        del request.headers['referer']
        request.headers['referer'] = cls.referer

        del request.headers["cache-control"]
        request.headers["cache-control"] = "no-cache"

        del request.headers['user-agent']
        request.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
        # request.headers['user-agent'] = 'Mozilla/5.0 (Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36'
        del request.headers['cookie']
        request.headers['cookie'] = cls._cookie_dict_in_str()

    @classmethod
    def response_interceptor(cls, request: Request, response: Response) -> None:
        for key, val in response.headers.items():
            if key == "set-cookie" or key == "Set-Cookie":
                cls._update_cookie_dict(text=val)

    @classmethod
    def _update_cookie_dict(cls, text: str) -> None:
        match = re.match(r"(?P<cookie>.+?);.*", text, flags=re.DOTALL)
        if match:
            cookie = match.group("cookie")
            cls._str_in_cookie_dict(cookie)

    @classmethod
    def _str_in_cookie_dict(cls, text: str) -> None:
        # метод text.split("=") не подходит, так как в значении cookies может быть знак "=", например:
        # _yasc=LsdFI8ooV1++Xd/aXDuyF3ZAzjLf2B971h9sDpzmWq9qaXBZgyhCcUMwZL44envByT8=
        match = re.match(r"(?P<key>.+?)=(?P<val>.*)", text)
        key, val = match.group("key"), match.group("val")
        if not cls.cookie_dict.get(key):
            cls.cookie_dict[key] = val

    @classmethod
    def _cookie_dict_in_str(cls) -> str:
        if cls.cookie_dict:
            result = ""
            for key, val in cls.cookie_dict.items():
                result += f"{key}={val}; "
            return result[0:-2]
        else:
            return ""
