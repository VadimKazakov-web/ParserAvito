from selenium.webdriver.common.by import By
import logging
from base import OpenUrl
import re


class OpenAnnouncement(OpenUrl):

    def __init__(self, url, driver):
        super().__init__(driver)
        self.url = url
        self.target_block = '.style__contentLeftWrapper___XzU0Nj'
        self.target_block_inner_html = None
        self.pattern_id = re.compile('data-marker="item-view/item-id">\D+?(?P<id>\d+?)</span>')
        self.data = {}
        logging.info("url: {}".format(self.url))

    def find_blocks(self):
        block = self.driver.find_element(by=By.CSS_SELECTOR, value=self.target_block)
        self.target_block_inner_html = block.get_attribute('innerHTML')
        return self.target_block_inner_html

    def collect_data(self, block):
        result_id = self.pattern_id.search(block)
        self.data['id'] = result_id.group("id")

    def parser_data(self):
        block = self.find_blocks()
        self.collect_data(block)

    def start(self):
        self.open_url()
        self.parser_data()
        # logging.info("data: {}".format(self.data))
        # logging.info("length data: {}".format(len(self.data)))