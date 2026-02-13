# -*- coding: utf-8 -*-
import logging
import traceback
import webbrowser
import selenium.common
from parser_avito_manager import ResultInHtml, TimeMeasurementMixin, SetupVarMixin
from parser_avito_manager.open_page import OpenPage
from parser_avito_manager.open_announcement import OpenAnnouncement
from parser_avito_manager.worker import Worker
from exceptions import BadInternetConnection, PushExit
from exceptions import PushStopButton
from objects import connector
from settings import *
from audio.audio_notes import AudioNotesMixin
from tkinter_frontend import HandlersClass


def open_pages(*args, **kwargs):
    """
    Открытие страниц и получение ссылок на объявления для дальнейшей работы
    """
    driver = kwargs.get("driver")
    links_dict = kwargs.get("links_dict")
    connector.update_info(text="Открываются страницы")
    instance = OpenPage(driver)
    worker = Worker(driver=driver, instance=instance, links_dict=links_dict,
                    start_method=instance.start)
    instance = worker.start()
    return instance.data


def open_announcement(*args, **kwargs):
    """
    Открытие объявлений и получение конечных результатов в self._total_data = instance.extraction_and_sorting()
    """
    driver = kwargs.get("driver")
    links = kwargs.get("links")
    connector.update_info(text="Открываются объявления")
    instance = OpenAnnouncement(driver, links)
    try:
        worker = Worker(driver=driver, instance=instance, links=links,
                        start_method=instance.start)
        instance = worker.start()
    finally:
        Worker.reset_time_start()
        return {
            "total_data": instance.extraction_and_sorting(),
            "count_new_row_in_database": instance.count_new_row_in_database,
        }


class ParserAvitoManager(SetupVarMixin, TimeMeasurementMixin):
    """
    Класс в котором заключена главная логика работы программы
    """

    def __init__(self):
        SetupVarMixin.__init__(self)
        self._total_data = None
        self._count_new_row_in_database = 0

    def _bond_methods(self):
        self.setup_var()
        connector.callbacks_for_start_prog()
        data = None
        try:
            links_announcement = open_pages(driver=self.driver, links_dict=self._links_dict)
            data = open_announcement(driver=self.driver, links=links_announcement)
        except selenium.common.exceptions.WebDriverException as err:
            logging.warning(err)
            connector.update_info(text="WebDriverException, Проверьте интернет соединение")
        except BadInternetConnection:
            logging.warning("bad connections in avito.ru")
            connector.update_info(text="Плохое соединение с www.avito.ru")
        except PushStopButton as err:
            logging.info(err)
            connector.update_info(text="Остановка")
        except Exception as err:
            traceback.print_exception(err)
            logging.warning("err in bond_methods()")
            logging.warning(err)
        finally:
            self._total_data = data.get("total_data")
            self._count_new_row_in_database = data.get("count_new_row_in_database")
            self._exit()
            connector.callbacks_for_stop_prog()

    def _exit(self):
        """
        Метод реализует корректное завершение программы
        """
        # Закрытие браузера
        self.driver.quit()
        if self._total_data:
            logging.info("new row in database: {}".format(self._count_new_row_in_database))
            result_in_html = ResultInHtml(file_name=self._file_name, default_filename=self._default_filename,
                                          data=self._total_data,
                                          count=self._count_new_row_in_database)
            # Запись результата в файл
            result_in_html()
            webbrowser.open(str(result_in_html.file_name))

    def start(self):
        """
        Запуск цикла программы, отлов нажатия кнопки "выход",
        отлов нетипичной ошибки в except Exception as err, и повторная инициализация перед новой итерации
        """
        while True:
            try:
                self._bond_methods()
            except PushExit as err:
                logging.info(err)
                break
            except Exception as err:
                connector.update_info(text=err)
                traceback.print_exception(err)
                self.__init__()
            else:
                self.__init__()
