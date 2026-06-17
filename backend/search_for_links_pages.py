# -*- coding: utf-8 -*-
from collections.abc import Generator
from selenium.webdriver.common.by import By
from seleniumwire.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement


def how_to_search(block: WebElement) -> WebElement:
    link = block.find_element(by=By.TAG_NAME, value='h2').find_element(by=By.TAG_NAME, value='a')
    return link


class SearchLinks:

    """
    Класс ищет ссылки на объявления со страницы
    """

    # целевой css селектор, где гипотетически находятся данные
    _target_block = '.iva-item-title-KE8A9'
    _url_root = 'https://www.avito.ru'

    def __init__(self, driver: Chrome):
        self._driver = driver

    def _find_blocks(self) -> list[WebElement]:
        """
        Поиск блока html по селектору
        """
        blocks = self._driver.find_elements(by=By.CSS_SELECTOR, value=self._target_block)
        return blocks

    def _collect_data(self, blocks: list[WebElement]) -> Generator[str, None, None]:
        """
        Получение ссылок на объявления со страницы
        """
        for block in blocks:
            link = how_to_search(block)
            yield self._url_root + link.get_dom_attribute('href')

    def __call__(self) -> Generator[str, None, None]:
        blocks = self._find_blocks()
        gen = self._collect_data(blocks)
        for elem in gen:
            yield elem
