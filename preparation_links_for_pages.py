import re


class PreparationLinksForPages:

    def __init__(self, url, pages):
        self.url = url
        self.pages = pages
        self.result = []

    def start(self):
        res = re.search('\?', self.url)
        if not res:
            self.url = self.url + '?'
        while self.pages > 1:
            self.result.insert(0, self.url + f'&p={self.pages}')
            self.pages -= 1
        self.result.insert(0, self.url)
