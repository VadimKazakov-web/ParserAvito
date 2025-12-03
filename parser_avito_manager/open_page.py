from selenium.webdriver.common.by import By
import logging
from parser_avito_manager.base import OpenUrl


class OpenPage(OpenUrl):

    def __init__(self, driver, widget, data_for_progres):
        super().__init__(driver, widget, data_for_progres)
        self.target_block = '.iva-item-title-KE8A9'

    def find_blocks(self):
        blocks = self._driver.find_elements(by=By.CSS_SELECTOR, value=self.target_block)
        return blocks

    def collect_data(self, blocks):
        for block in blocks:
            link = block.find_element(by=By.TAG_NAME, value='h2').find_element(by=By.TAG_NAME, value='a')
            self._data.append({
                "title": link.get_dom_attribute('title'),
                "link": self._url_root + link.get_dom_attribute('href'),
            })

    def start(self, url):
        self._data = []
        logging.info("url: {}".format(url))
        super().start(url)
        logging.info("data: {}".format(self.data))
        logging.info("length data: {}".format(len(self.data)))

