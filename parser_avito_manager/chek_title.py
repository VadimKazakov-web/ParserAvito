import re
import logging
import time


class CheckTitleClass:

    def __init__(self):
        self._pattern_404 = re.compile(r'\b404\b')
        self._pattern_problem_ip = re.compile(r'Доступ ограничен')
        self._show_problem_ip_title = False

    def check_title(self, title):
        while True:
            if self._pattern_problem_ip.search(title):

                if not self._show_problem_ip_title:
                    logging.info("\npage title: {}".format(title))
                    self._show_problem_ip_title = True
                time.sleep(3)

            elif self._pattern_404.search(title):
                logging.info("\npage title: {}".format(title))
                return
            else:
                break
