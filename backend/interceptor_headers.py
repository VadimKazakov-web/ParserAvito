# -*- coding: utf-8 -*-
import re
from seleniumwire.request import Request, Response
from settings import COOKIE_FILE


def read_file(path):
    with open(path, "r") as file:
        text = file.read()
        return text


class InterceptorHeaders:

    """
    Класс актуализирует cookies в запросах, используются возможности seleniumwire.
    https://github.com/wkeeling/selenium-wire#:~:text=Selenium%20Wire-,Selenium%20Wire,-extends%20Selenium%27s%20Python
    """

    referer = 'https://www.avito.ru'

    def __init__(self, read_cookie=True):
        if read_cookie:
            self.cookie_dict = self.setup_cookie()
        else:
            self.cookie_dict = {}

    def setup_cookie(self):
        cookie_dict = {}
        try:
            text = read_file(COOKIE_FILE)
        except FileNotFoundError:
            return cookie_dict
        else:
            cookie_list = text.split("; ")
            for pair in cookie_list:
                self._set_cookie(pair, cookie_dict)
            return cookie_dict

    def write_cookie(self):
        text = self._dict_in_str(self.cookie_dict)
        with open(COOKIE_FILE, "w") as file:
            file.write(text)

    def request_interceptor(self, request: Request) -> None:

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
        request.headers['referer'] = self.referer

        del request.headers["cache-control"]
        request.headers["cache-control"] = "no-cache"

        del request.headers['user-agent']
        request.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'

        del request.headers['cookie']
        request.headers['cookie'] = self._dict_in_str(self.cookie_dict)

    def response_interceptor(self, request: Request, response: Response) -> None:
        for key, val in response.headers.items():
            if key == "set-cookie" or key == "Set-Cookie":
                self._update_cookie_dict(text=val, dict_obj=self.cookie_dict)

    def _update_cookie_dict(self, text: str, dict_obj: dict) -> None:
        match = re.match(r"(?P<cookie>.+?);.*", text, flags=re.DOTALL)
        if match:
            cookie = match.group("cookie")
            self._set_cookie(cookie, dict_obj)

    @staticmethod
    def _set_cookie(text: str, dict_obj: dict) -> None:
        # метод text.split("=") не подходит, так как в значении cookies может быть знак "=", например:
        # _yasc=LsdFI8ooV1++Xd/aXDuyF3ZAzjLf2B971h9sDpzmWq9qaXBZgyhCcUMwZL44envByT8=
        match = re.match(r"(?P<key>.+?)=(?P<val>.*)", text)
        key, val = match.group("key"), match.group("val")
        if not dict_obj.get(key):
            dict_obj[key] = val

    @staticmethod
    def _dict_in_str(dict_obj: dict) -> str:
        if dict_obj:
            result = ""
            for key, val in dict_obj.items():
                result += f"{key}={val}; "
            return result[0:-2]
        else:
            return ""
