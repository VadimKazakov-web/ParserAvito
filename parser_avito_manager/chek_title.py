# -*- coding: utf-8 -*-
import re
import logging
import time
from audio.audio_notes import AudioNotesMixin
from exceptions import BreakWhile
from objects import connector


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
        from parser_avito_manager.worker import check_chanel
        while True:
            if cls._pattern_problem_ip.search(driver.title):
                text = "page title: {}".format(driver.title)
                connector.update_info(text=text)
                check_chanel()
                if not cls._show_problem_ip_title:
                    logging.info(text)
                    cls._show_problem_ip_title = True
                time.sleep(3)

            elif cls._pattern_404.search(driver.title):
                raise BreakWhile
            else:
                cls._show_problem_ip_title = False
                return None
