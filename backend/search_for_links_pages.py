# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from seleniumwire.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement


def how_to_search(block: WebElement) -> WebElement:
    link = block.find_element(by=By.TAG_NAME, value='h2').find_element(by=By.TAG_NAME, value='a')
    return link


class SearchLinks:
    # целевой css селектор, где гипотетически находятся данные
    _target_block = '.iva-item-title-KE8A9'
    _target_block_xpath = '/html/body/div[1]/div/div[1]/div/div/div/div[3]/div/div/div/div/div/div[5]/div/div/div/a'
    _url_root = 'https://www.avito.ru'
    # _url_root = 'https://m.avito.ru'

    def __init__(self, driver: Chrome):
        self._driver = driver

    def _find_blocks(self) -> list[WebElement]:
        """
        Поиск блока html по селектору
        """
        blocks = self._driver.find_elements(by=By.CSS_SELECTOR, value=self._target_block)
        return blocks

    def _find_blocks_xpath(self) -> list[WebElement]:
        """
        Поиск блока html по полному xpath
        """
        blocks = self._driver.find_elements(by=By.XPATH, value=self._target_block_xpath)
        return blocks

    def _collect_data(self, blocks: list[WebElement]) -> list[str]:
        """
        Получение ссылок на объявления со страницы
        """
        for block in blocks:
            link = how_to_search(block)
            yield self._url_root + link.get_dom_attribute('href')

    def _collect_data_for_xpath(self, blocks: list[WebElement]) -> list[str]:
        """
        Получение ссылок на объявления со страницы
        """
        for block in blocks:
            yield self._url_root + block.get_dom_attribute('href')

    def __call__(self) -> list[str]:
        # blocks = self._find_blocks_xpath()
        # gen = self._collect_data_for_xpath(blocks)
        blocks = self._find_blocks()
        gen = self._collect_data(blocks)
        for elem in gen:
            yield elem
