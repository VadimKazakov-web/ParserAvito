# -*- coding: utf-8 -*-
from backend.open_url import OpenUrl


class OpenAdvertisement(OpenUrl):
    """
    Класс реализует открытие каждого объявления
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _open(self) -> None:
        self._driver.execute_script(f"window.open('{self._url}', '_blank');")

    def _switch_to(self):
        self._driver.switch_to.window(self._driver.window_handles[1])

    def __call__(self, *args, **kwargs):
        return super().__call__()
