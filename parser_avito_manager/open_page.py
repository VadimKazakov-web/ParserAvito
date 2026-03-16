from selenium.webdriver.common.by import By
import logging
from parser_avito_manager.base import OpenUrl


class OpenPage(OpenUrl):
    """
    Класс работает со страницами
    """

    def __init__(self, driver):
        super().__init__(driver)
        # целевой css селектор, где гипотетически находятся данные
        self.target_block = '.iva-item-title-KE8A9'
        self._data = []

    def _find_blocks(self):
        """
        Поиск блока html по селектору
        """
        blocks = self._driver.find_elements(by=By.CSS_SELECTOR, value=self.target_block)
        return blocks

    def _collect_data(self, blocks):
        """
        Получение ссылок на обьявления со страницы
        """
        data = []
        for block in blocks:
            link = block.find_element(by=By.TAG_NAME, value='h2').find_element(by=By.TAG_NAME, value='a')
            data.append(self._url_root + link.get_dom_attribute('href'))
        return data

    def start(self, url: str) -> list:
        data = super().start(url)
        return data
