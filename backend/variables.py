# -*- coding: utf-8 -*-
from settings import BASE_DIR, WIDTH_LABEL
import textwrap


def check_var(data: dict):
    url, pages, filename = data.get("url"), data.get("pages"), data.get("filename")
    if url and pages and filename:
        variables = data
        variables["filename"] = BASE_DIR / filename
        return variables


class Variables:

    def __init__(self, data):
        self.variables = check_var(data)
        self.width_label = WIDTH_LABEL

    def get_url(self) -> str:
        value = self.variables.get("url")
        return value

    def get_pages(self) -> int:
        value = self.variables.get("pages")
        return value

    def get_filename(self) -> str:
        value = self.variables.get("filename")
        return value

