import logging
import time
import webbrowser
from preparation_links_for_pages import PreparationLinksForPages
from result_in_html import ResultInHtml
from open_page import OpenPage
from open_announcement import OpenAnnouncement
from selenium import webdriver


def setup_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.timeouts = {"pageLoad": 30000}
    options.page_load_strategy = 'eager'
    # options.browser_version = 'stable'
    options.browser_version = '142'
    # assert options.capabilities['browserVersion'] == 'stable'
    assert options.capabilities['browserVersion'] == '142'
    driver = webdriver.Chrome(options=options)
    return driver


class ParserAvitoManager:

    def __init__(self, url, file_name, pages, test=None, timeout=2):
        self.test = test
        self.url = url
        self.pages = pages
        self.links = None
        self.file_name = file_name
        self.total_data = []
        self.driver = setup_options()
        self.driver.implicitly_wait(60)
        self.timeout = timeout
        self.counter = 0

    def preparation_links(self):
        prep_links_instance = PreparationLinksForPages(url=self.url, pages=self.pages)
        prep_links_instance.start()
        self.links = prep_links_instance.result

    def __enter__(self):
        return self

    def open_pages(self):
        worker = OpenPage(self.driver)
        for url in self.links:
            worker.start(url)
            self.total_data.extend(worker.data)

    def open_announcement(self):
        worker = OpenAnnouncement(driver=self.driver)
        if self.test:
            data_list = self.total_data[0:10]
        else:
            data_list = self.total_data

        length_data_list = len(data_list)
        for elem in data_list:
            url = elem.get("link")
            worker.start(url)
            elem.update(worker.data)
            time.sleep(self.timeout)
            self.counter += 1
            print(f'\rотсканировано объявлений: {self.counter}/{length_data_list}', end='')
        print('\n')

    def sort_total_data(self):
        self.total_data.sort(key=lambda e: e.get("total_views", 0), reverse=True)

    def start(self):
        self.preparation_links()
        self.open_pages()
        self.open_announcement()
        self.sort_total_data()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
        logging.info("+++ total data: {}".format(self.total_data))
        logging.info("+++ length total data: {}".format(len(self.total_data)))
        pattern = ResultInHtml()
        pattern.write_result(file_name=self.file_name, data=self.total_data)
        webbrowser.open(self.file_name)
