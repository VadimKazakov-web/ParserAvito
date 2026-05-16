# -*- coding: utf-8 -*-
import logging
import selenium.common
from selenium.webdriver.common.by import By
import re
from settings import LEFT_BLOCK_ANNOUNCEMENT_CSS, RIGHT_BLOCK_ANNOUNCEMENT_CSS
from seleniumwire.webdriver import Chrome


class CollectData:
    """
    Класс собирает данные с объявления
    """
    target_block_left = {"block": LEFT_BLOCK_ANNOUNCEMENT_CSS, "name": "left"}
    target_block_right = {"block": RIGHT_BLOCK_ANNOUNCEMENT_CSS, "name": "right"}
    pattern_id = re.compile(r'data-marker="item-view/item-id">\D+?(?P<id>\d+?)\D', flags=re.DOTALL)
    pattern_date = re.compile(r'data-marker="item-view/item-date">.*?·(?P<date>.+?)</span>', flags=re.DOTALL)
    pattern_total_views = re.compile(r'data-marker="item-view/total-views">(?P<total_views>\d+?)\D+?</span>',
                                          flags=re.DOTALL)
    pattern_today_views = re.compile(r'data-marker="item-view/today-views">.+?(?P<today_views>\d+?)\D+?</span>',
                                          flags=re.DOTALL)
    pattern_title = re.compile(r'<h1.+?data-marker="item-view/title-info">(?P<title>.+?)</h1>', flags=re.DOTALL)
    pattern_rating = re.compile(r'<meta.+?"ratingValue" content="(?P<rating>.+?)">', flags=re.DOTALL)
    pattern_reviews = re.compile(r'<a data-marker="rating-caption/rating".+?>(?P<reviews>\d*?)\D*?</a>',
                                      flags=re.DOTALL)
    counter_stale_element_exception = 3

    def __init__(self, driver: Chrome):
        self._driver = driver

    @classmethod
    def _find_block(cls, driver: Chrome, target_block: str) -> str:
        """
        Поиск блока html по селектору
        """
        counter = cls.counter_stale_element_exception
        while counter:
            try:
                block = driver.find_element(by=By.CSS_SELECTOR, value=target_block)
                html = block.get_attribute('innerHTML')
            except selenium.common.exceptions.StaleElementReferenceException:
                logging.warning("StaleElementReferenceException in\nfind_block(self)")
                counter -= 1
            else:
                return html

    @classmethod
    def _find_blocks(cls, driver) -> dict:
        """
        Поиск левого и правого блока html по селектору
        """
        data = {}
        for target in cls.target_block_left, cls.target_block_right:
            html = cls._find_block(driver=driver, target_block=target.get("block"))
            data[target.get("name")] = html
        return data

    def _collect_data(self, blocks: dict) -> dict | None:
        """
        Поиск нужных данных на странице обьявления
        """
        block_left, block_right = blocks.get("left"), blocks.get("right")
        result = {}
        end_point = None
        result_title = self.pattern_title.search(block_left)
        if result_title:
            title = result_title.group("title")
            result["title"] = title
            # используются end_point на html странице, для поиска по шаблону по "цепочке"
            end_point = result_title.end()

        result_id = self.pattern_id.search(block_left[end_point:])
        if result_id:
            result['id'] = result_id.group("id")
            end_point = result_id.end()
        else:
            logging.info("url without id: {}".format(self._driver.current_url))
            return

        result_date = self.pattern_date.search(block_left[end_point:])
        if result_date:
            result['date'] = result_date.group("date").strip()
            end_point = result_date.end()

        result_total_views = self.pattern_total_views.search(block_left[end_point:])
        if result_total_views:
            result['total_views'] = int(result_total_views.group("total_views"))
            end_point = result_total_views.end()
        else:
            result['total_views'] = 0

        result_today_views = self.pattern_today_views.search(block_left[end_point:])
        if result_today_views:
            result['today_views'] = int(result_today_views.group("today_views"))
        else:
            result['today_views'] = 0

        result_rating = self.pattern_rating.search(block_right)
        if result_rating:
            result["rating"] = float(result_rating.group("rating"))
            end_point = result_rating.end()
        else:
            result["rating"] = 0.0
            end_point = 0

        result_reviews = self.pattern_reviews.search(block_right[end_point:])
        if result_reviews:
            result["reviews"] = int(result_reviews.group("reviews"))
        else:
            result["reviews"] = 0

        result["link"] = self._driver.current_url
        return result

    def __call__(self) -> dict:
        data = self._find_blocks(self._driver)
        result = self._collect_data(data)
        return result
