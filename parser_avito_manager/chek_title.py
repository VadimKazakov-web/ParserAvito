import re
import logging
import time


class CheckTitleMixin:

    _pattern_404 = re.compile(r'\b404\b')
    _pattern_problem_ip = re.compile(r'Доступ ограничен')
    _show_problem_ip_title = False

    @classmethod
    def check_title(cls, driver):
        while True:
            if cls._pattern_problem_ip.search(driver.title):

                if not cls._show_problem_ip_title:
                    logging.info("\npage title: {}".format(driver.title))
                    cls._show_problem_ip_title = True
                time.sleep(3)

            elif cls._pattern_404.search(driver.title):
                logging.info("\npage title: {}".format(driver.title))
                return "404"
            else:
                break
