import logging
from selenium.webdriver.common.by import By
from parser_avito_manager.base import OpenUrl
import re


class OpenAnnouncement(OpenUrl):

    def __init__(self, driver):
        super().__init__(driver)
        self.target_block = '.style__contentLeftWrapper___XzU0Nj'
        self.target_block_inner_html = None
        self.pattern_id = re.compile(r'data-marker="item-view/item-id">\D+?(?P<id>\d+?)</span>',
                                     flags=re.DOTALL)
        self.pattern_date = re.compile(r'data-marker="item-view/item-date">.+?-->(?P<date>.+?)</span>')
        self.pattern_total_views = re.compile(r'data-marker="item-view/total-views">(?P<total_views>\d+?)\D+?</span>')
        self.pattern_today_views = re.compile(r'data-marker="item-view/today-views">.+?(?P<today_views>\d+?)\D+?</span>')

    def find_blocks(self):
        block = self._driver.find_element(by=By.CSS_SELECTOR, value=self.target_block)
        self.target_block_inner_html = block.get_attribute('innerHTML')
        return self.target_block_inner_html

    def collect_data(self, block):
        result_id = self.pattern_id.search(block)
        if result_id:
            self._data['id'] = result_id.group("id")

        result_date = self.pattern_date.search(block)
        if result_date:
            self._data['date'] = result_date.group("date")

        result_total_views = self.pattern_total_views.search(block)
        if result_total_views:
            self._data['total_views'] = int(result_total_views.group("total_views"))

        result_today_views = self.pattern_today_views.search(block)
        if result_today_views:
            self._data['today_views'] = int(result_today_views.group("today_views"))

    def start(self):
        self._data = {}
        super().start()
