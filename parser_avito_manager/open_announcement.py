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
        self.target_block_seller = '.style__contentRightWrapper___XzU0Nj'
        self.target_block_seller_html = None
        self.pattern = re.compile(r'data-marker="item-view/item-id">\D+?(?P<id>\d+?)</span>'
                                  r'.+?data-marker="item-view/item-date">.+?-->(?P<date>.+?)</span>'
                                  r'.*?<span(.+?data-marker="item-view/total-views">(?P<total_views>\d+?)\D+?</span>)?'
                                  r'.*?<span(.+?data-marker="item-view/today-views">.+?'
                                  r'(?P<today_views>\d+?)\D+?</span>)?', flags=re.DOTALL)
        self.pattern_id = re.compile(r'data-marker="item-view/item-id">\D+?(?P<id>\d+?)\D', flags=re.DOTALL)
        self.pattern_date = re.compile(r'data-marker="item-view/item-date">.*?·.*?(?P<date>.+?)</span>', flags=re.DOTALL)
        self.pattern_total_views = re.compile(r'data-marker="item-view/total-views">(?P<total_views>\d+?)\D+?</span>', flags=re.DOTALL)
        self.pattern_today_views = re.compile(r'data-marker="item-view/today-views">.+?(?P<today_views>\d+?)\D+?</span>', flags=re.DOTALL)
        self.pattern_title = re.compile(r'<h1.+?data-marker="item-view/title-info">(?P<title>.+?)</h1>', flags=re.DOTALL)
        self.pattern_rating = re.compile(r'<meta.+?"ratingValue" content="(?P<rating>.+?)">', flags=re.DOTALL)
        self.pattern_reviews = re.compile(r'<a data-marker="rating-caption/rating".+?>(?P<reviews>\d*?)\D*?</a>', flags=re.DOTALL)
        self.counter_stale_element_exception = 3

    def find_blocks(self):
        counter = self.counter_stale_element_exception
        while counter:
            try:
                block = self._driver.find_element(by=By.CSS_SELECTOR, value=self.target_block)
                self.target_block_inner_html = block.get_attribute('innerHTML')
            except selenium.common.exceptions.StaleElementReferenceException:
                logging.warning("StaleElementReferenceExceptionin\nfind_blocks(self) block")
                counter -= 1
            else:
                break

        counter = self.counter_stale_element_exception
        while counter:
            try:
                block_seller = self._driver.find_element(by=By.CSS_SELECTOR, value=self.target_block_seller)
                self.target_block_seller_html = block_seller.get_attribute('innerHTML')
            except selenium.common.exceptions.StaleElementReferenceException:
                logging.warning("StaleElementReferenceExceptionin\nfind_blocks(self) block_seller")
                counter -= 1
            else:
                break

        return self.target_block_inner_html, self.target_block_seller_html

    def collect_data(self, blocks):
        block, block_seller = blocks
        data = {}
        end_point = None
        result_title = self.pattern_title.search(block)
        if result_title:
            title = result_title.group("title")
            data["title"] = title
            end_point = result_title.end()

        result_id = self.pattern_id.search(block[end_point:])
        if result_id:
            data['id'] = result_id.group("id")
            end_point = result_id.end()

        result_date = self.pattern_date.search(block[end_point:])
        if result_date:
            data['date'] = result_date.group("date")
            end_point = result_date.end()

        result_total_views = self.pattern_total_views.search(block[end_point:])
        if result_total_views:
            data['total_views'] = int(result_total_views.group("total_views"))
            end_point = result_total_views.end()

        result_today_views = self.pattern_today_views.search(block[end_point:])
        if result_today_views:
            data['today_views'] = int(result_today_views.group("today_views"))

        result_rating = self.pattern_rating.search(block_seller)
        if result_rating:
            data["rating"] = float(result_rating.group("rating"))
            end_point = result_rating.end()

        result_reviews = self.pattern_reviews.search(block_seller[end_point:])
        if result_reviews:
            data["reviews"] = result_reviews.group("reviews")

        data["link"] = self._url
        self._data.append(data)

    def start(self, url: str):
        self._url = url
        super().start(url)
