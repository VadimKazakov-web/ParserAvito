import time

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


class OpenPagesManager:

    def __init__(self, links, test=None, timeout=2):
        self.test = test
        self.links = links
        self.total_data = []
        self.driver = setup_options()
        self.driver.implicitly_wait(60)
        self.timeout = timeout

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

        for elem in data_list:
            url = elem.get("link")
            worker.start(url)
            elem.update(worker.data)
            time.sleep(self.timeout)

    def sort_total_data(self):
        self.total_data.sort(key=lambda e: e.get("total_views", 0), reverse=True)

    def start(self):
        self.open_pages()
        self.open_announcement()
        self.sort_total_data()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
