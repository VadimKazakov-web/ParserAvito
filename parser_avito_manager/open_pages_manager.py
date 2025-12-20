import functools
import logging
import time
import webbrowser
import selenium.common
from parser_avito_manager import PreparationLinksForPages, ResultInHtml, CheckTitleMixin, TimeMeasurementMixin
from parser_avito_manager.open_page import OpenPage
from parser_avito_manager.open_announcement import OpenAnnouncement
from selenium import webdriver
from exceptions import BadInternetConnection
from tkinter_frontend.window_root.frame_1.start_button.build import active_inactive_start_button
from tkinter_frontend.window_root.frame_1.stop_button.build import active_inactive_stop_button
import queue
from exceptions import PushStopButton
from objects import connector


def setup_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.timeouts = {"pageLoad": 30000}
    options.page_load_strategy = 'eager'
    options.browser_version = 'stable'
    # assert options.capabilities['browserVersion'] == 'stable'
    # assert options.capabilities['browserVersion'] == '142'
    driver = webdriver.Chrome(options=options)
    return driver


class ParserAvitoManager(CheckTitleMixin, TimeMeasurementMixin):

    def __init__(self, channel_for_variables: queue,
                 data_for_progress, test=None, timeout=3):
        self.test = test
        self.url = None
        self.pages = None
        self.links = None
        self.file_name = None
        self.channel_for_variables = channel_for_variables
        self.data_for_progress = data_for_progress
        self.data_from_tk = None
        self.widget_tk = None
        self.sorting = None
        self.total_data = []
        self.driver = None
        self.timeout = timeout
        self.counter = 0
        self.timeout_exceptions_counter = 4

    def accepting_variables(self):
        self.data_from_tk = self.channel_for_variables.get()
        self.setup_variables()

    def check_chanel(self):
        try:
            data = self.channel_for_variables.get(block=False)
        except queue.Empty:
            return
        else:
            if data == "push_stop_button":
                raise PushStopButton

    def setup_variables(self):
        if not isinstance(self.data_from_tk, str):
            self.url = self.data_from_tk.get("link")
            self.file_name = self.data_from_tk.get("filename")
            self.pages = int(self.data_from_tk.get("count_pages"))
            self.widget_tk = self.data_from_tk.get("widget_tk")
            self.sorting = self.data_from_tk.get("sorting")

    def preparation_links(self):
        prep_links_instance = PreparationLinksForPages(url=self.url, pages=self.pages)
        prep_links_instance.start()
        self.links = prep_links_instance.result

    def update_progress(self, links):
        length = len(links)
        self.counter += 1
        progress_text = f'отсканировано объявлений: {self.counter}/{length} ({round(self.counter / length * 100)}%)'
        connector.update_progress(widget=self.widget_tk, text=progress_text)

    def worker(self, instance, links, callback=None):
        if callback:
            callback_func = callback
        else:
            callback_func = lambda a=None: a
        for url in links:
            timeout_exceptions_counter = self.timeout_exceptions_counter
            try:
                self.check_chanel()
            except PushStopButton:
                if isinstance(instance, OpenAnnouncement):
                    self.total_data = instance.data
                raise PushStopButton
            while timeout_exceptions_counter:
                try:
                    self.driver.get(url)
                    time.sleep(self.timeout)
                except selenium.common.exceptions.TimeoutException:
                    self.bad_connection_audio()
                    logging.warning("TimeoutException")
                    timeout_exceptions_counter -= 1
                    connector.update_info(widget=self.widget_tk, text="Плохое соединение, перезагружаю страницу,\n"
                                                                      "осталось попыток: {}".format(timeout_exceptions_counter))
                    self.bad_connection_audio()
                except Exception as err:
                    print(err)
                else:
                    connector.update_title(widget=self.widget_tk, text=self.driver.title)
                    if self.check_title(self.driver) == CheckTitleMixin.not_found:
                        self.page_not_found_audio()
                        break
                    else:
                        instance.start(url)
                    callback_func(links)
                    break
            else:
                connector.update_info(widget=self.widget_tk, text="Плохое соединение с www.avito.ru")
                raise BadInternetConnection

    def open_pages(self):
        connector.update_info(widget=self.widget_tk, text="Открываются страницы")
        instance = OpenPage(self.driver)
        self.worker(instance=instance, links=self.links)
        return instance.data

    def open_announcement(self, links):
        connector.update_info(widget=self.widget_tk, text="Открываются объявления")
        instance = OpenAnnouncement(self.driver)
        self.worker(instance=instance, links=links, callback=self.update_progress)
        self.total_data = instance.data

    def sort_total_data(self):
        connector.update_info(widget=self.widget_tk, text="Выполняется сортировка")
        if self.sorting == "total_views":
            self.total_data.sort(key=lambda e: e.get("total_views", 0), reverse=True)
        elif self.sorting == "today_views":
            self.total_data.sort(key=lambda e: e.get("today_views", 0), reverse=True)
        elif self.sorting == "reviews":
            self.total_data.sort(key=lambda e: e.get("reviews", 0), reverse=True)

    def start(self):
        self.driver = setup_options()
        self.driver.implicitly_wait(60)
        self.accepting_variables()
        logging.info("data from tk: {}".format(self.data_from_tk))
        self.preparation_links()
        active_inactive_start_button.make_inactive_button()
        connector.update_progress(widget=self.widget_tk, text="...")
        connector.update_title(widget=self.widget_tk, text="...")
        try:
            self.time_measurement_start()
            active_inactive_stop_button.make_active_button()
            links = self.open_pages()
            self.open_announcement(links)
        except selenium.common.exceptions.WebDriverException as err:
            logging.warning(err)
            connector.update_info(widget=self.widget_tk, text="WebDriverException, Проверьте интернет соединение")
            raise BadInternetConnection
        except BadInternetConnection:
            connector.update_info(widget=self.widget_tk, text="Плохое соединение с www.avito.ru")
            raise BadInternetConnection
        except PushStopButton:
            logging.info("push stop button")
            connector.update_info(widget=self.widget_tk, text="Выполнена остановка")
        except Exception as err:
            connector.update_info(widget=self.widget_tk, text=err)
        finally:
            self.exit()
            self.time_measurement_end()
            connector.update_title(widget=self.widget_tk,
                                   text="Время работы программы {}".format(self.time_measurement_result()))
            active_inactive_start_button.make_active_button()
            active_inactive_stop_button.make_inactive_button()

    def exit(self):
        self.driver.quit()
        if self.total_data:
            self.sort_total_data()
            logging.info("+++ scanned: {} +++".format(self.counter))
            pattern = ResultInHtml()
            pattern.write_result(file_name=self.file_name, data=self.total_data, count=self.counter)
            connector.update_info(widget=self.widget_tk, text="Результаты готовы")
            webbrowser.open(self.file_name)
            self.complete_audio()
