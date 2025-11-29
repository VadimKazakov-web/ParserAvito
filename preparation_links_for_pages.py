import re


class PreparationLinksForPages:

    def __init__(self, url, pages):
        self._url = url
        self._pages = pages
        self._result = []

    @property
    def result(self):
        return self._result

    def start(self):
        res = re.search(r'[?]', self._url)
        if res:
            url = self._url
        else:
            url = self._url + '?'
        while self._pages > 1:
            self._result.insert(0, url + f'&p={self._pages}')
            self._pages -= 1
        self._result.insert(0, self._url)
