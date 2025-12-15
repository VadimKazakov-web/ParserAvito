import logging
import time
import webbrowser
import selenium.common
from parser_avito_manager import PreparationLinksForPages, ResultInHtml, CheckTitleMixin
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


class ParserAvitoManager(CheckTitleMixin):

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

    def open_pages(self):
        worker = OpenPage(self.driver)
        for url in self.links:
            timeout_exceptions_counter = self.timeout_exceptions_counter
            connector.update_info(widget=self.widget_tk, text="Открываются страницы")
            while timeout_exceptions_counter:
                try:
                    self.driver.get(url)
                    connector.update_title(widget=self.widget_tk, text=self.driver.title)
                    if self.check_title(self.driver) == CheckTitleMixin.not_found:
                        break
                    else:
                        worker.start()
                except selenium.common.exceptions.TimeoutException:
                    logging.warning("TimeoutException in open_pages(self)")
                    timeout_exceptions_counter -= 1
                    connector.update_info(widget=self.widget_tk, text="Плохое соединение, перезагружаю страницу,\n"
                                                                      "осталось попыток: {}".format(timeout_exceptions_counter))
                else:
                    connector.update_info(widget=self.widget_tk, text="Открываются страницы")
                    self.total_data.extend(worker.data)
                    time.sleep(self.timeout)
                    break
            else:
                connector.update_info(widget=self.widget_tk, text="Плохое соединение с www.avito.ru")
                raise BadInternetConnection

    def open_announcement(self):
        active_inactive_stop_button.make_active_button()
        worker = OpenAnnouncement(driver=self.driver)
        length_data_list = len(self.total_data)
        for elem in self.total_data:
            url = elem.get("link")
            try:
                self.check_chanel()
            except PushStopButton:
                logging.info("push stop button")
                return
            connector.update_info(widget=self.widget_tk, text="Открываются объявления")
            timeout_exceptions_counter = self.timeout_exceptions_counter
            while timeout_exceptions_counter:
                try:
                    self.driver.get(url)
                    connector.update_title(widget=self.widget_tk, text=self.driver.title)
                    if self.check_title(self.driver) == CheckTitleMixin.not_found:
                        break
                    else:
                        worker.start()
                except selenium.common.exceptions.TimeoutException:
                    logging.warning("TimeoutException in open_announcement(self)")
                    timeout_exceptions_counter -= 1
                    connector.update_info(widget=self.widget_tk, text="Плохое соединение, перезагружаю страницу,\n"
                                                                      "осталось попыток: {}".format(timeout_exceptions_counter))
                else:
                    elem.update(worker.data)
                    self.counter += 1
                    progress_text = f'отсканировано объявлений: {self.counter}/{length_data_list} ({round(self.counter / length_data_list * 100)}%)'
                    connector.update_progress(widget=self.widget_tk, text=progress_text)
                    time.sleep(self.timeout)
                    if self.counter % 10 == 0:
                        time.sleep(self.timeout)
                    break
            else:
                connector.update_info(widget=self.widget_tk, text="Плохое соединение с www.avito.ru")
                raise BadInternetConnection

    def sort_total_data(self):
        connector.update_info(widget=self.widget_tk, text="Выполняется сортировка")
        if self.sorting == "total_views":
            self.total_data.sort(key=lambda e: e.get("total_views", 0), reverse=True)
        elif self.sorting == "today_views":
            self.total_data.sort(key=lambda e: e.get("today_views", 0), reverse=True)

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
            self.open_pages()
            self.open_announcement()
        except selenium.common.exceptions.WebDriverException as err:
            logging.warning(err)
            connector.update_info(widget=self.widget_tk, text="WebDriverException, Проверьте интернет соединение")
            raise BadInternetConnection
        except BadInternetConnection:
            connector.update_info(widget=self.widget_tk, text="Плохое соединение с www.avito.ru")
            raise BadInternetConnection
        finally:
            self.exit()
            active_inactive_start_button.make_active_button()
            active_inactive_stop_button.make_inactive_button()

    def exit(self):
        self.driver.quit()
        self.sort_total_data()
        logging.info("+++ length total data: {}".format(len(self.total_data)))
        pattern = ResultInHtml()
        pattern.write_result(file_name=self.file_name, data=self.total_data, count=self.counter)
        connector.update_info(widget=self.widget_tk, text="Результаты готовы")
        webbrowser.open(self.file_name)
