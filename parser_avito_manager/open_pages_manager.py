import logging
import time
import webbrowser
import selenium.common
from parser_avito_manager import PreparationLinksForPages, ResultInHtml
from parser_avito_manager.open_page import OpenPage
from parser_avito_manager.open_announcement import OpenAnnouncement
from selenium import webdriver
import queue
from exceptions import BadInternetConnection
import math


def setup_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.timeouts = {"pageLoad": 30000}
    options.page_load_strategy = 'eager'
    options.browser_version = 'stable'
    # options.browser_version = '142'
    # assert options.capabilities['browserVersion'] == 'stable'
    # assert options.capabilities['browserVersion'] == '142'
    driver = webdriver.Chrome(options=options)
    return driver


class ParserAvitoManager:

    def __init__(self, channel_for_variables: queue,
                 data_for_progress, test=None, timeout=6):
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
        data = self.channel_for_variables.get()
        self.data_from_tk = data
        self.setup_variables()

    def setup_variables(self):
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
        worker = OpenPage(self.driver, self.widget_tk, self.data_for_progress)
        for url in self.links:
            counter = self.timeout_exceptions_counter
            while counter:
                try:
                    worker.start(url)
                except selenium.common.exceptions.TimeoutException:
                    logging.info("TimeoutException in open_pages(self)")
                    counter -= 1
                else:
                    self.total_data.extend(worker.data)
                    time.sleep(4)
                    break
            else:
                self.data_for_progress.set(key="page_title", val="Плохое соединение с www.avito.ru")
                self.widget_tk.event_generate("<<UpdateProgress>>")
                raise BadInternetConnection

    def open_announcement(self):
        worker = OpenAnnouncement(driver=self.driver, widget=self.widget_tk,
                                  data_for_progress=self.data_for_progress)
        if self.test:
            data_list = self.total_data[0:10]
        else:
            data_list = self.total_data

        length_data_list = len(data_list)
        for elem in data_list:
            url = elem.get("link")
            counter = self.timeout_exceptions_counter
            while counter:
                try:
                    worker.start(url)
                except selenium.common.exceptions.TimeoutException as err:
                    logging.info("TimeoutException in open_announcement(self)")
                    counter -= 1
                else:
                    elem.update(worker.data)
                    self.counter += 1
                    progress_text = f'отсканировано объявлений: {self.counter}/{length_data_list} ({round(self.counter / length_data_list * 100)}%)'
                    # key=text - прогресс выполнения
                    # key=page_title - заголовок страницы
                    self.data_for_progress.set(key="text", val=progress_text)
                    self.widget_tk.event_generate("<<UpdateProgress>>")
                    time.sleep(4)
                    if self.counter % 10 == 0:
                        time.sleep(self.timeout)
                    break
            else:
                self.data_for_progress.set(key="page_title", val="Плохое соединение с www.avito.ru")
                self.widget_tk.event_generate("<<UpdateProgress>>")
                raise BadInternetConnection

    def sort_total_data(self):
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
        try:
            self.open_pages()
            self.open_announcement()
        except selenium.common.exceptions.WebDriverException as err:
            logging.warning(err)
            self.data_for_progress.set(key="page_title", val="Проверьте интернет соединение")
            self.widget_tk.event_generate("<<UpdateProgress>>")
            raise BadInternetConnection
        finally:
            self.sort_total_data()
            self.exit()

    def exit(self):
        self.driver.quit()
        logging.info("+++ length total data: {}".format(len(self.total_data)))
        pattern = ResultInHtml()
        pattern.write_result(file_name=self.file_name, data=self.total_data)
        webbrowser.open(self.file_name)
