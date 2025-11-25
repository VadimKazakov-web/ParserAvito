import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging

FORMAT = '[%(asctime)s]%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

URL = 'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc'
URL_MOBILE = 'https://m.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc'


def setup_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    # options.browser_version = 'stable'
    options.browser_version = '142'
    # assert options.capabilities['browserVersion'] == 'stable'
    assert options.capabilities['browserVersion'] == '142'
    driver = webdriver.Chrome(options=options)
    return driver


class OpenPage:

    def __init__(self, url):
        self.url = url
        self.driver = setup_options()
        self.driver.implicitly_wait(60)
        self.title = None
        self.target_block = '.iva-item-title-KE8A9'
        self.data = []

    def open_url(self):
        counter = 3
        while counter:
            try:
                self.driver.get(self.url)
            except urllib3.exceptions.ReadTimeoutError:
                counter -= 1
            else:
                return

    def get_title(self):
        title = self.driver.title
        self.title = title

    def find_blocks(self):
        blocks = self.driver.find_elements(by=By.CSS_SELECTOR, value=self.target_block)
        return blocks

    def collect_data(self, blocks):
        for block in blocks:
            link = block.find_element(by=By.TAG_NAME, value='h2').find_element(by=By.TAG_NAME, value='a')
            self.data.append({
                "title": link.text,
                "link": link.get_dom_attribute('href'),
            })

    def parser_data(self):
        blocks = self.find_blocks()
        self.collect_data(blocks)

    def start(self):
        self.open_url()
        self.parser_data()
        self.driver.quit()
        logging.info("data: {}".format(self.data))
        logging.info("length data: {}".format(len(self.data)))


worker = OpenPage(URL)
worker.start()
