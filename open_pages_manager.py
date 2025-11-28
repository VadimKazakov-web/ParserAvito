from open_page import OpenPage
from open_announcement import OpenAnnouncement
from selenium import webdriver


def setup_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.page_load_strategy = 'eager'
    # options.browser_version = 'stable'
    options.browser_version = '142'
    # assert options.capabilities['browserVersion'] == 'stable'
    assert options.capabilities['browserVersion'] == '142'
    driver = webdriver.Chrome(options=options)
    return driver


class OpenPagesManager:

    def __init__(self, links, test=None):
        self.test = test
        self.links = links
        self.total_data = []
        self.driver = setup_options()
        self.driver.implicitly_wait(60)

    def __enter__(self):
        return self

    def open_pages(self):
        for url in self.links:
            worker = OpenPage(url=url, driver=self.driver)
            worker.start()
            self.total_data.extend(worker.data)

    def open_announcement(self):
        if self.test:
            for elem in self.total_data[0:10]:
                url = elem.get("link")
                worker = OpenAnnouncement(url=url, driver=self.driver)
                worker.start()
                elem.update(worker.data)
        else:
            for elem in self.total_data:
                url = elem.get("link")
                worker = OpenAnnouncement(url=url, driver=self.driver)
                worker.start()
                elem.update(worker.data)

    def start(self):
        self.open_pages()
        self.open_announcement()
        for elem in self.total_data:
            print(elem)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
