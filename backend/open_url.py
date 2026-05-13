# -*- coding: utf-8 -*-
import time
from seleniumwire.webdriver import Chrome
from backend import CheckTitleMixin
from backend.utils.close_popup import CloseAuthPopupMixin
from backend.utils.timeout import TimeoutMixin


class OpenUrl(CloseAuthPopupMixin, TimeoutMixin, CheckTitleMixin):

    """
    Базовый класс для открытия web-страницы
    """

    def __init__(self, driver: Chrome, url: str, update_title_callback=lambda driver: None,
                 events_handler=lambda: None, *args, **kwargs):
        super(OpenUrl, self).__init__(driver)
        self._driver = driver
        self._url = url
        self._update_title = update_title_callback
        self._events_handler = events_handler

    def _open(self):
        self._driver.get(self._url)

    def _work_gen(self):
        yield True
        self._checking_number_tabs(3)
        yield True
        self._open()
        yield True
        # переключиться на новую вкладку
        self._switch_to()
        yield True
        self._update_title(self._driver)
        yield True
        if not self.check_title(self._driver):
            self._driver.close()
            return False
        else:
            self._update_title(self._driver)
            yield True
            # закрытия всплывающего окна с предложением авторизоваться, если оно есть
            self.close_popup()
            yield True
            # задержка случайным таймаутом
            self.timeout()
            return True

    def __call__(self, *args, **kwargs) -> bool:
        gen = self._work_gen()
        while True:
            try:
                next(gen)
                self._events_handler()
            except StopIteration as err:
                if not err.value:
                    return False
                else:
                    return True

    def _switch_to(self):
        pass

    def _checking_number_tabs(self, num):
        if len(self._driver.window_handles) > num:
            print("emergency closure window: lots of tabs {}".format(num))
            self._driver.quit()
