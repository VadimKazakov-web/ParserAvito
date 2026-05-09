import re


class PreparationLinksForPages:

    """
    Класс из базового url создаёт ссылки на страницы
    """

    def __init__(self, url, pages):
        self._url = url
        self._pages = pages
        self._result = []
        self._result_dict = {}

    @property
    def result(self):
        return self._result

    @property
    def result_dict(self):
        return self._result_dict

    @staticmethod
    def _check_url(url):
        res = None
        match = re.search(r'[?]', url)
        if match:
            res = url
        else:
            res = url + '?'
        return res

    def _create_result_dict(self):
        url = self._check_url(self._url)
        count = 1
        while count <= self._pages:
            self._result_dict[count] = url + f'&p={count}'
            count += 1

    def start(self):
        self._create_result_dict()
        return self._result_dict
