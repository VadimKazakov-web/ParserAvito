import logging

import selenium.common
from selenium.webdriver.common.by import By
from parser_avito_manager.base import OpenUrl
import re


class OpenAnnouncement(OpenUrl):

    def __init__(self, driver):
        super().__init__(driver)
        self._data = []
        self.target_block = '.style__contentLeftWrapper___XzU0Nj'
        self.target_block_inner_html = None
        self.pattern = re.compile(r'data-marker="item-view/item-id">\D+?(?P<id>\d+?)</span>'
                                  r'.+?data-marker="item-view/item-date">.+?-->(?P<date>.+?)</span>'
                                  r'.*?<span(.+?data-marker="item-view/total-views">(?P<total_views>\d+?)\D+?</span>)?'
                                  r'.*?<span(.+?data-marker="item-view/today-views">.+?'
                                  r'(?P<today_views>\d+?)\D+?</span>)?', flags=re.DOTALL)
        self.pattern_title = re.compile(r'<h1.+?data-marker="item-view/title-info">(?P<title>.+?)</h1>')
        self.counter_stale_element_exception = 3

    def find_blocks(self):
        counter = self.counter_stale_element_exception
        while counter:
            try:
                block = self._driver.find_element(by=By.CSS_SELECTOR, value=self.target_block)
                self.target_block_inner_html = block.get_attribute('innerHTML')
            except selenium.common.exceptions.StaleElementReferenceException:
                logging.warning("selenium.common.exceptions.StaleElementReferenceExceptionin\nfind_blocks(self)")
                counter -= 1
            else:
                return self.target_block_inner_html
        return None

    def collect_data(self, block):
        data = {}
        result_title = self.pattern_title.search(block)
        if result_title:
            title = result_title.group("title")
            data["title"] = title
        result = self.pattern.search(block)
        if result:
            result_id = result.group("id")
            if result_id:
                data['id'] = result_id
            result_date = result.group("date")
            if result_date:
                data['date'] = result_date
            result_total_views = result.group("total_views")
            if result_total_views:
                data['total_views'] = int(result_total_views)
            result_today_views = result.group("today_views")
            if result_today_views:
                data['today_views'] = int(result_today_views)
            data["link"] = self._url
            self._data.append(data)

    def start(self, url: str):
        self._url = url
        super().start(url)
