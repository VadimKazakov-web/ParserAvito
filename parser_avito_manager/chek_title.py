# -*- coding: utf-8 -*-
import re
import logging
import time
from audio.audio_notes import AudioNotesMixin
from exceptions import BreakWhile


class CheckTitleMixin(AudioNotesMixin):

    """
    Класс для проверки заголовка страницы
    """

    _pattern_404 = re.compile(r'\b404\b')
    _pattern_problem_ip = re.compile(r'Доступ ограничен')
    _show_problem_ip_title = False
    _not_found = 404

    @classmethod
    def check_title(cls, driver):
        while True:
            if cls._pattern_problem_ip.search(driver.title):

                if not cls._show_problem_ip_title:
                    logging.info("\npage title: {}".format(driver.title))
                    cls._show_problem_ip_title = True
                    # cls.access_restricted_audio()
                time.sleep(3)

            elif cls._pattern_404.search(driver.title):
                logging.info("\npage title: {}".format(driver.title))
                # cls.page_not_found_audio()
                raise BreakWhile
            else:
                return None
