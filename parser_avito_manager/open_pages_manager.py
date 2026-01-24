# -*- coding: utf-8 -*-
import logging
import traceback
import webbrowser
import selenium.common
from parser_avito_manager import PreparationLinksForPages, ResultInHtml, TimeMeasurementMixin
from parser_avito_manager.open_page import OpenPage
from parser_avito_manager.open_announcement import OpenAnnouncement
from parser_avito_manager.worker import Worker
from selenium import webdriver
from exceptions import BadInternetConnection, PushExit, BreakWhile
from exceptions import PushStopButton
from objects import connector
from settings import *
from audio.audio_notes import AudioNotesMixin
from tkinter_frontend import HandlersClass


class ParserAvitoManager(TimeMeasurementMixin, AudioNotesMixin, HandlersClass):

    def __init__(self):
        self.driver = None
        self._url = None
        self._pages = None
        self._links_pages = None
        self._links_announcement = None
        self._file_name = None
        self._data_from_tk = None
        self._total_data = []
        self._base_dir = BASE_DIR
        self._count_new_row_in_database = 0
        self._count_update_row_in_database = 0
        self._counter = 0

    @staticmethod
    def setup_options():
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.timeouts = {"pageLoad": 30000}
        options.page_load_strategy = 'eager'
        options.browser_version = 'stable'
        # assert options.capabilities['browserVersion'] == 'stable'
        # assert options.capabilities['browserVersion'] == '142'
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(60)
        return driver

    def _accepting_variables(self):
        self._data_from_tk = connector.channel_for_variables.get()
        logging.info("data from tk: {}".format(self._data_from_tk))
        if isinstance(self._data_from_tk, dict):
            self._setup_variables()
        elif self._data_from_tk == "exit":
            self.driver.quit()
            raise PushExit

    def _setup_variables(self):
        self._url = self._data_from_tk.get("link")
        filename = self._data_from_tk.get("filename")
        self._file_name = self._base_dir / Path(filename)
        self._pages = int(self._data_from_tk.get("count_pages"))

    def _preparation_links(self):
        prep_links_instance = PreparationLinksForPages(url=self._url, pages=self._pages)
        prep_links_instance.start()
        self._links_pages = prep_links_instance.result

    def _open_pages(self):
        connector.update_info(text="Открываются страницы")
        instance = OpenPage(self.driver)
        worker = Worker(driver=self.driver, instance=instance, links=self._links_pages)
        instance = worker.start()
        return instance.data

    def _open_announcement(self, links):
        connector.update_info(text="Открываются объявления")
        instance = OpenAnnouncement(self.driver, links)
        try:
            worker = Worker(driver=self.driver, instance=instance, links=self._links_announcement)
            instance = worker.start()
        finally:
            Worker.reset_time_start()
            self._total_data = instance.extraction_and_sorting()
            self._counter = instance.counter
            self._count_new_row_in_database = instance.count_new_row_in_database
            self._count_update_row_in_database = instance.count_update_row_in_database

    def _sort_total_data(self, top):
        length = len(self._total_data)
        connector.update_info(text="Выполняется сортировка")
        if length < top:
            top = length
        result = {
            "total_views": sorted(self._total_data, key=lambda e: e.get("total_views", 0), reverse=True)[0:top],
            "today_views": sorted(self._total_data, key=lambda e: e.get("today_views", 0), reverse=True)[0:top],
            "reviews": sorted(self._total_data, key=lambda e: e.get("reviews", 0), reverse=True)[0:top],
        }
        self._total_data = result

    def _bond_methods(self):
        self.driver = self.setup_options()
        self._accepting_variables()
        self._initial_text()
        connector.callbacks_for_start_prog()
        self._preparation_links()
        try:
            self._links_announcement = self._open_pages()
            self._open_announcement(self._links_announcement)
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
            self._exit()
            connector.callbacks_for_stop_prog()

    def _exit(self):
        self.driver.quit()
        if self._total_data:
            # self._sort_total_data(top=TOP_ANNOUNCEMENT)
            logging.info("+++ scanned: {} +++".format(self._counter))
            logging.info("new row in database: {}".format(self._count_new_row_in_database))
            logging.info("update row in database: {}".format(self._count_update_row_in_database))
            result_in_html = ResultInHtml()
            try:
                result_in_html.write_result(file_name=self._file_name, data=self._total_data, count=self._counter)
            except OSError as err:
                self._file_name = BASE_DIR / self.default_filename()
                text_info = "rename filename in default: {}".format(self._file_name)
                logging.warning(err)
                logging.warning(text_info)
                connector.update_info(text=text_info)
                result_in_html.write_result(file_name=self._file_name, data=self._total_data, count=self._counter)
            else:
                connector.update_info(text="Результаты готовы")
            finally:
                webbrowser.open(str(self._file_name))
                # self.complete_audio()

    def _initial_text(self):
        logging.info("")
        logging.info("-" * 40)
        logging.info("start parser")
        logging.info("base dir: {}".format(BASE_DIR))
        logging.info("filename: {}".format(self._file_name))
        logging.info("database dir: {}, "
                     "\n\tdatabase: {}".format(DATABASE_DIR, DATABASE))

    def start(self):
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
