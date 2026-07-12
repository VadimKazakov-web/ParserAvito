# -*- coding: utf-8 -*-
import logging
from seleniumwire.webdriver import Chrome
from backend import CheckTitleMixin
from backend.utils.close_popup import CloseAuthPopupMixin
from backend.utils.timeout import TimeoutMixin
from exceptions.main import PushExit


class OpenUrl(CloseAuthPopupMixin, TimeoutMixin, CheckTitleMixin):

    """
    Базовый класс для открытия web-страницы
    """

    PAGE_NOT_FOUND = "page not found"

    def __init__(self, driver: Chrome, url: str):
        self._driver = driver
        self._url = url

    def _open(self):
        self._driver.get(self._url)

    async def _work_gen(self):
        self._checking_number_tabs(3)
        self._open()
        yield
        # переключиться на новую вкладку
        self._switch_to()
        yield
        if not self.check_title(self._driver):
            self._driver.close()
            yield self.PAGE_NOT_FOUND
        yield
        # закрытия всплывающего окна с предложением авторизоваться, если оно есть
        self.close_popup(self._driver)
        # задержка случайным таймаутом
        # await self.timeout()

    async def __call__(self, *args, **kwargs) -> bool | str:
        async for result in self._work_gen():
            if result:
                return result

    def _switch_to(self):
        pass

    def _checking_number_tabs(self, num):
        if len(self._driver.window_handles) > num:
            self._driver.quit()
            text = "emergency closure window: lots of tabs {}".format(num)
            logging.warning(text)
            raise PushExit(text)
