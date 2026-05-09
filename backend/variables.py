# -*- coding: utf-8 -*-
from settings import BASE_DIR, WIDTH_LABEL
import textwrap


class BaseVariables:
    variables = {}
    info = None
    width_label = WIDTH_LABEL


class Variables(BaseVariables):

    def __init__(self):
        self.variables = super().variables

    @classmethod
    def set_info(cls, *args, **kwargs):
        # https://docs.python.org/3/library/textwrap.html#textwrap.TextWrapper.wrap
        data = textwrap.fill(text=args[0], width=cls.width_label)
        cls.info = data

    @classmethod
    def get_info(cls):
        return cls.info

    @classmethod
    def set_var(cls, data: dict):
        url, pages, filename = data.get("url"), data.get("pages"), data.get("filename")
        if url and pages and filename:
            cls.variables["url"] = url
            cls.variables["pages"] = pages
            cls.variables["filename"] = BASE_DIR / filename
            return True

    @classmethod
    def get_url(cls) -> str:
        value = cls.variables.get("url")
        return value

    @classmethod
    def get_pages(cls) -> int:
        value = cls.variables.get("pages")
        return value

    @classmethod
    def get_filename(cls) -> str:
        value = cls.variables.get("filename")
        return value

