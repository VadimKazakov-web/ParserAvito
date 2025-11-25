import urllib3
from selenium.webdriver.common.by import By
import logging
from base import OpenUrl


class OpenPage(OpenUrl):

    def __init__(self, url, driver):
        super().__init__(driver)
        self.url = url
        self.target_block = '.iva-item-title-KE8A9'
        logging.info("url: {}".format(self.url))

    def open_url(self):
        counter = 3
        while counter:
            try:
                self.driver.get(self.url)
            except urllib3.exceptions.ReadTimeoutError:
                counter -= 1
            else:
                return

    def find_blocks(self):
        blocks = self.driver.find_elements(by=By.CSS_SELECTOR, value=self.target_block)
        return blocks

    def collect_data(self, blocks):
        for block in blocks:
            link = block.find_element(by=By.TAG_NAME, value='h2').find_element(by=By.TAG_NAME, value='a')
            self.data.append({
                "title": link.get_dom_attribute('title'),
                "link": self.url_root + link.get_dom_attribute('href'),
            })

    def parser_data(self):
        blocks = self.find_blocks()
        self.collect_data(blocks)

    def start(self):
        self.open_url()
        self.parser_data()
        logging.info("data: {}".format(self.data))
        logging.info("length data: {}".format(len(self.data)))

