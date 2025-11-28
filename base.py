import urllib3


class OpenUrl:

    def __init__(self, driver):
        self.url = None
        self.driver = driver
        self.data = []
        self.url_root = 'https://www.avito.ru'

    def open_url(self):
        counter = 3
        while counter:
            try:
                self.driver.get(self.url)
            except urllib3.exceptions.ReadTimeoutError:
                counter -= 1
            else:
                return

