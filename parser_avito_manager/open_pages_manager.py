# -*- coding: utf-8 -*-
import logging
import time
import traceback
import webbrowser
import selenium.common
from parser_avito_manager import PreparationLinksForPages, ResultInHtml, CheckTitleMixin, TimeMeasurementMixin
from parser_avito_manager.open_page import OpenPage
from parser_avito_manager.open_announcement import OpenAnnouncement
from selenium import webdriver
from exceptions import BadInternetConnection, PushExit, BreakWhile
from tkinter_frontend.window_root.frame_1.start_button.build import active_inactive_start_button
from tkinter_frontend.window_root.frame_1.stop_button.build import active_inactive_stop_button
import queue
from exceptions import PushStopButton
from objects import connector
from settings import *


def check_chanel():
    try:
        data = connector.channel_for_variables.get(block=False)
    except queue.Empty:
        return
    else:
        if data == "push_stop_button":
            raise PushStopButton


class ParserAvitoManager(CheckTitleMixin, TimeMeasurementMixin):

    def __init__(self):
        self.driver = self.setup_options()
        self._url = None
        self._pages = None
        self._links_pages = None
        self._links_announcement = None
        self._file_name = None
        self._data_from_tk = None
        self._total_data = []
        self._timeout = TIMEOUT
        self._timeout_exceptions_counter = TIMEOUT_EXCEPTIONS_COUNTER
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

    def _driver_and_timeout(self, url):
        check_chanel()
        self.driver.get(url)
        check_chanel()
        time.sleep(self._timeout / 2)
        check_chanel()
        time.sleep(self._timeout / 2)

    def _worker(self, instance, links):
        for url in links:
            timeout_exceptions_counter = self._timeout_exceptions_counter
            while timeout_exceptions_counter:
                try:
                    self._driver_and_timeout(url)
                    self.check_title(self.driver)
                except selenium.common.exceptions.TimeoutException:
                    logging.warning("TimeoutException")
                    connector.update_info(text="Плохое соединение, "
                                                                      "перезагружаю страницу,\n"
                                                                      "осталось попыток: {}"
                                          .format(timeout_exceptions_counter))
                    timeout_exceptions_counter -= 1
                except BreakWhile as err:
                    logging.info(err)
                    break
                else:
                    connector.update_info(text="Продолжаю открывать web-страницы")
                    connector.update_title(text=self.driver.title)
                    data = instance.start(url)
                    break
            else:
                connector.update_info(text="Плохое соединение с www.avito.ru")
                raise BadInternetConnection

    def _open_pages(self):
        connector.update_info(text="Открываются страницы")
        instance = OpenPage(self.driver)
        self._worker(instance=instance, links=self._links_pages)
        return instance.data

    def _open_announcement(self, links):
        connector.update_info(text="Открываются объявления")
        instance = OpenAnnouncement(self.driver, links)
        try:
            self._worker(instance=instance, links=links)
        finally:
            self._total_data = instance.data
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
        self._accepting_variables()
        active_inactive_start_button.make_inactive_button()
        active_inactive_stop_button.make_active_button()
        self._preparation_links()
        connector.update_progress(text="...")
        connector.update_title(text="...")
        try:
            self._links_pages = self._open_pages()
            self._open_announcement(self._links_pages)
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
            logging.warning("err in bond_methods()")
            logging.warning(err)
        finally:
            self._exit()
            active_inactive_start_button.make_active_button()
            active_inactive_stop_button.make_inactive_button()

    def _exit(self):
        self.driver.quit()
        if self._total_data:
            self._sort_total_data(top=TOP_ANNOUNCEMENT)
            logging.info("+++ scanned: {} +++".format(self._counter))
            logging.info("new row in database: {}".format(self._count_new_row_in_database))
            logging.info("update row in database: {}".format(self._count_update_row_in_database))
            result_in_html = ResultInHtml()
            result_in_html.write_result(file_name=self._file_name, data=self._total_data, count=self._counter)
            connector.update_info(text="Результаты готовы")
            webbrowser.open(self._file_name)
            self.complete_audio()

    @staticmethod
    def _initial_text():
        logging.info("")
        logging.info("-" * 40)
        logging.info("start parser")

    def start(self):
        while True:
            self.time_measurement_start()
            self._initial_text()
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
                self.time_measurement_end()
                connector.update_title(text="Время работы программы {}".format(self.time_measurement_result()))
                self.__init__()
