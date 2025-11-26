from open_page import OpenPage
from selenium import webdriver


def setup_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    # options.browser_version = 'stable'
    options.browser_version = '142'
    # assert options.capabilities['browserVersion'] == 'stable'
    assert options.capabilities['browserVersion'] == '142'
    driver = webdriver.Chrome(options=options)
    return driver


class OpenPagesManager:

    def __init__(self, links):
        self.links = links
        self.total_data = []
        self.driver = setup_options()
        self.driver.implicitly_wait(60)

    def __enter__(self):
        return self

    def start(self):
        for url in self.links:
            worker = OpenPage(url=url, driver=self.driver)
            worker.start()
            self.total_data.extend(worker.data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
