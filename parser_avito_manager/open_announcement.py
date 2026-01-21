import logging
import selenium.common
from selenium.webdriver.common.by import By

from objects import connector
from parser_avito_manager.base import OpenUrl
import re
from parser_avito_manager.database import DataBaseMixin


class OpenAnnouncement(OpenUrl, DataBaseMixin):

    def __init__(self, driver, links):
        super().__init__(driver)
        DataBaseMixin.__init__(self)
        self.links = links
        self._length_links = len(self.links)
        self._data = []
        self._target_block = {"block": '.style__contentLeftWrapper___XzU0Nj', "name": "left"}
        self._target_block_seller = {"block": '.style__contentRightWrapper___XzU0Nj', "name": "right"}
        self.pattern_id = re.compile(r'data-marker="item-view/item-id">\D+?(?P<id>\d+?)\D', flags=re.DOTALL)
        self.pattern_date = re.compile(r'data-marker="item-view/item-date">.*?·.*?(?P<date>.+?)</span>', flags=re.DOTALL)
        self.pattern_total_views = re.compile(r'data-marker="item-view/total-views">(?P<total_views>\d+?)\D+?</span>', flags=re.DOTALL)
        self.pattern_today_views = re.compile(r'data-marker="item-view/today-views">.+?(?P<today_views>\d+?)\D+?</span>', flags=re.DOTALL)
        self.pattern_title = re.compile(r'<h1.+?data-marker="item-view/title-info">(?P<title>.+?)</h1>', flags=re.DOTALL)
        self.pattern_rating = re.compile(r'<meta.+?"ratingValue" content="(?P<rating>.+?)">', flags=re.DOTALL)
        self.pattern_reviews = re.compile(r'<a data-marker="rating-caption/rating".+?>(?P<reviews>\d*?)\D*?</a>', flags=re.DOTALL)
        self.counter_stale_element_exception = 3
        self.counter = 0

    def find_block(self, target_block):
        counter = self.counter_stale_element_exception
        while counter:
            try:
                block = self._driver.find_element(by=By.CSS_SELECTOR, value=target_block)
                html = block.get_attribute('innerHTML')
            except selenium.common.exceptions.StaleElementReferenceException:
                logging.warning("StaleElementReferenceExceptionin\nfind_block(self)")
                counter -= 1
            else:
                return html

    def find_blocks(self):
        data = {}
        for target in self._target_block, self._target_block_seller:
            html = self.find_block(target_block=target.get("block"))
            data[target.get("name")] = html
        return data

    def collect_data(self, blocks):
        block, block_seller = blocks.get("left"), blocks.get("right")
        result = {}
        end_point = None
        result_title = self.pattern_title.search(block)
        if result_title:
            title = result_title.group("title")
            result["title"] = title
            end_point = result_title.end()

        result_id = self.pattern_id.search(block[end_point:])
        if result_id:
            result['id'] = result_id.group("id")
            end_point = result_id.end()
        else:
            logging.info("url without id: {}".format(self._url))
            return

        result_date = self.pattern_date.search(block[end_point:])
        if result_date:
            result['date'] = result_date.group("date")
            end_point = result_date.end()

        result_total_views = self.pattern_total_views.search(block[end_point:])
        if result_total_views:
            result['total_views'] = int(result_total_views.group("total_views"))
            end_point = result_total_views.end()

        result_today_views = self.pattern_today_views.search(block[end_point:])
        if result_today_views:
            result['today_views'] = int(result_today_views.group("today_views"))

        result_rating = self.pattern_rating.search(block_seller)
        if result_rating:
            result["rating"] = float(result_rating.group("rating"))
            end_point = result_rating.end()
        else:
            result["rating"] = 0.0
            end_point = 0

        result_reviews = self.pattern_reviews.search(block_seller[end_point:])
        if result_reviews:
            result["reviews"] = int(result_reviews.group("reviews"))
        else:
            result["reviews"] = 0

        result["link"] = self._url
        self._data.append(result)
        return result

    def _update_progress(self):
        self.counter += 1
        progress_text = f'отсканировано объявлений: {self.counter}/{self._length_links} ({round(self.counter / self._length_links * 100)}%)'
        connector.update_progress(text=progress_text)

    def start(self, url: str):
        self._url = url
        blocks = self.find_blocks()
        if blocks:
            data = self.collect_data(blocks)
            if data:
                self.record_in_database(data)
                self._update_progress()
                return data
