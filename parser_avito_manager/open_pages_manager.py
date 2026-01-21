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
from parser_avito_manager.database import DataBaseMixin


def check_chanel():
    try:
        data = connector.channel_for_variables.get(block=False)
    except queue.Empty:
        return
    else:
        if data == "push_stop_button":
            raise PushStopButton


class ParserAvitoManager(CheckTitleMixin, TimeMeasurementMixin, DataBaseMixin):

    def __init__(self):
        DataBaseMixin.__init__(self)
        self.url = None
        self.pages = None
        self.links = None
        self.file_name = None
        self.data_from_tk = None
        self.widget_tk = None
        self.sorting = None
        self.total_data = []
        self.driver = self.setup_options()
        self.timeout = TIMEOUT
        self.counter = 0
        self.timeout_exceptions_counter = TIMEOUT_EXCEPTIONS_COUNTER
        self.base_dir = BASE_DIR
        self.cursor = None
        self.connection = None

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

    def accepting_variables(self):
        self.data_from_tk = connector.channel_for_variables.get()
        logging.info("data from tk: {}".format(self.data_from_tk))
        if isinstance(self.data_from_tk, dict):
            self.setup_variables()
        elif self.data_from_tk == "exit":
            self.driver.quit()
            raise PushExit

    def setup_variables(self):
        self.url = self.data_from_tk.get("link")
        filename = self.data_from_tk.get("filename")
        self.file_name = self.base_dir / Path(filename)
        self.pages = int(self.data_from_tk.get("count_pages"))
        self.widget_tk = self.data_from_tk.get("widget_tk")
        self.sorting = self.data_from_tk.get("sorting")

    def preparation_links(self):
        prep_links_instance = PreparationLinksForPages(url=self.url, pages=self.pages)
        prep_links_instance.start()
        self.links = prep_links_instance.result

    def update_progress(self, links: list) -> None:
        length = len(links)
        self.counter += 1
        progress_text = f'отсканировано объявлений: {self.counter}/{length} ({round(self.counter / length * 100)}%)'
        connector.update_progress(widget=self.widget_tk, text=progress_text)

    def driver_and_timeout(self, url):
        check_chanel()
        self.driver.get(url)
        check_chanel()
        time.sleep(self.timeout / 2)
        check_chanel()
        time.sleep(self.timeout / 2)

    def worker(self, instance, links, callback=None):
        for url in links:
            timeout_exceptions_counter = self.timeout_exceptions_counter
            while timeout_exceptions_counter:
                try:
                    self.driver_and_timeout(url)
                    self.check_title(self.driver)
                except selenium.common.exceptions.TimeoutException:
                    logging.warning("TimeoutException")
                    connector.update_info(widget=self.widget_tk, text="Плохое соединение, "
                                                                      "перезагружаю страницу,\n"
                                                                      "осталось попыток: {}"
                                          .format(timeout_exceptions_counter))
                    timeout_exceptions_counter -= 1
                except BreakWhile as err:
                    logging.info(err)
                    break
                else:
                    connector.update_info(widget=self.widget_tk, text="Продолжаю открывать web-страницы")
                    connector.update_title(widget=self.widget_tk, text=self.driver.title)
                    data = instance.start(url)
                    callback(links)
                    break
            else:
                connector.update_info(widget=self.widget_tk, text="Плохое соединение с www.avito.ru")
                raise BadInternetConnection

    def open_pages(self):
        connector.update_info(widget=self.widget_tk, text="Открываются страницы")
        instance = OpenPage(self.driver)
        self.worker(instance=instance, links=self.links, callback=lambda a=None: a)
        return instance.data

    def open_announcement(self, links):
        connector.update_info(widget=self.widget_tk, text="Открываются объявления")
        instance = OpenAnnouncement(self.driver)
        try:
            self.worker(instance=instance, links=links, callback=self.update_progress)
        finally:
            self.total_data = instance.data
            self.count_new_row_in_database = instance.count_new_row_in_database
            self.count_update_row_in_database = instance.count_update_row_in_database

    def sort_total_data(self, top):
        length = len(self.total_data)
        if length < top:
            top = length
        result = {
            "total_views": sorted(self.total_data, key=lambda e: e.get("total_views", 0), reverse=True)[0:top],
            "today_views": sorted(self.total_data, key=lambda e: e.get("today_views", 0), reverse=True)[0:top],
            "reviews": sorted(self.total_data, key=lambda e: e.get("reviews", 0), reverse=True)[0:top],
        }
        self.total_data = result
        connector.update_info(widget=self.widget_tk, text="Выполняется сортировка")

    def bond_methods(self):
        self.count_row_in_database()
        self.accepting_variables()
        active_inactive_start_button.make_inactive_button()
        active_inactive_stop_button.make_active_button()
        self.preparation_links()
        connector.update_progress(widget=self.widget_tk, text="...")
        connector.update_title(widget=self.widget_tk, text="...")
        try:
            links = self.open_pages()
            self.open_announcement(links)
        except selenium.common.exceptions.WebDriverException as err:
            logging.warning(err)
            connector.update_info(widget=self.widget_tk, text="WebDriverException, Проверьте интернет соединение")
        except BadInternetConnection:
            logging.warning("bad connections in avito.ru")
            connector.update_info(widget=self.widget_tk, text="Плохое соединение с www.avito.ru")
        except PushStopButton as err:
            logging.info(err)
            connector.update_info(widget=self.widget_tk, text="Остановка")
        except Exception as err:
            logging.warning("err in bond_methods()")
            logging.warning(err)
        finally:
            self.exit()
            active_inactive_start_button.make_active_button()
            active_inactive_stop_button.make_inactive_button()

    def exit(self):
        self.driver.quit()
        if self.total_data:
            self.sort_total_data(top=TOP_ANNOUNCEMENT)
            logging.info("+++ scanned: {} +++".format(self.counter))
            logging.info("new row in database: {}".format(self.count_new_row_in_database))
            logging.info("update row in database: {}".format(self.count_update_row_in_database))
            result_in_html = ResultInHtml()
            result_in_html.write_result(file_name=self.file_name, data=self.total_data, count=self.counter)
            connector.update_info(widget=self.widget_tk, text="Результаты готовы")
            webbrowser.open(self.file_name)
            self.complete_audio()

    @staticmethod
    def initial_text():
        logging.info("")
        logging.info("")
        logging.info("-" * 20)
        logging.info("start parser")

    def start(self):
        while True:
            self.time_measurement_start()
            self.initial_text()
            try:
                self.bond_methods()
            except PushExit as err:
                logging.info(err)
                break
            except Exception as err:
                connector.update_info(widget=self.widget_tk, text=err)
                traceback.print_exception(err)
            else:
                self.time_measurement_end()
                connector.update_title(widget=self.widget_tk,
                                       text="Время работы программы {}".format(self.time_measurement_result()))
            finally:
                self.__init__()




