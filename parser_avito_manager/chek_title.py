import re
import logging
import time


class CheckTitleClass:

    def __init__(self, driver, widget, data_for_progress):
        self.widget = widget
        self.data_for_progress = data_for_progress
        self._driver = driver
        self._pattern_404 = re.compile(r'\b404\b')
        self._pattern_problem_ip = re.compile(r'Доступ ограничен')
        self._show_problem_ip_title = False

    def check_title(self):
        while True:
            self.data_for_progress.set("page_title", self._driver.title)
            self.widget.event_generate("<<UpdateProgress>>")
            if self._pattern_problem_ip.search(self._driver.title):

                if not self._show_problem_ip_title:
                    logging.info("\npage title: {}".format(self._driver.title))
                    self._show_problem_ip_title = True
                time.sleep(3)

            elif self._pattern_404.search(self._driver.title):
                logging.info("\npage title: {}".format(self._driver.title))
                return "404"
            else:
                break
