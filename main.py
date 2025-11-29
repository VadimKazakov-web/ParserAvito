import logging
from open_pages_manager import ParserAvitoManager

FORMAT = '[%(asctime)s]%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

PAGES = 2
URL = 'https://www.avito.ru/moskva/predlozheniya_uslug/delovye_uslugi/konsultirovanie-ASgBAgICAkSYC7KfAZ4L~J8B?716=10201'
FILE_NAME = 'result.html'

with ParserAvitoManager(file_name=FILE_NAME, url=URL, pages=PAGES, test=False) as manager:
    manager.start()
