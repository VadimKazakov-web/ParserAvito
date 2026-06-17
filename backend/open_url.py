# -*- coding: utf-8 -*-
from seleniumwire.webdriver import Chrome
from backend import CheckTitleMixin
from backend.utils.close_popup import CloseAuthPopupMixin
from backend.utils.timeout import TimeoutMixin


class OpenUrl(CloseAuthPopupMixin, TimeoutMixin, CheckTitleMixin):
    page_not_found = "page_not_found"

    """
    Базовый класс для открытия web-страницы
    """

    def __init__(self, driver: Chrome, url: str):
        super(OpenUrl, self).__init__(driver)
        self._driver = driver
        self._url = url

    def _open(self):
        self._driver.get(self._url)

    def _work_gen(self):
        self._checking_number_tabs(3)
        self._open()
        yield 
        # переключиться на новую вкладку
        self._switch_to()
        yield
        if not self.check_title(self._driver):
            self._driver.close()
            return self.page_not_found
        yield
        # закрытия всплывающего окна с предложением авторизоваться, если оно есть
        self.close_popup()
        # задержка случайным таймаутом
        yield from self.timeout()
        return True

    def __call__(self, *args, **kwargs) -> bool:
        result = yield from self._work_gen()
        return result

    def _switch_to(self):
        pass

    def _checking_number_tabs(self, num):
        if len(self._driver.window_handles) > num:
            print("emergency closure window: lots of tabs {}".format(num))
            self._driver.quit()
