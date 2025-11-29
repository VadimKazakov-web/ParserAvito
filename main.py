import logging
from preparation_links_for_pages import PreparationLinksForPages
from open_pages_manager import OpenPagesManager
from result_in_html import ResultInHtml
import webbrowser

FORMAT = '[%(asctime)s]%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

PAGES = 2
URL = 'https://www.avito.ru/moskva/predlozheniya_uslug/delovye_uslugi/konsultirovanie-ASgBAgICAkSYC7KfAZ4L~J8B?716=10201'
FILE_NAME = 'result_service.html'

prep_links_instance = PreparationLinksForPages(url=URL, pages=PAGES)
prep_links_instance.start()
links_pages = prep_links_instance.result

with OpenPagesManager(links=links_pages, test=False) as manager:
    manager.start()
    total_data = manager.total_data
    logging.info("+++++++ total data: {}".format(total_data))
    logging.info("+++++++ length total data: {}".format(len(total_data)))

    pattern = ResultInHtml()
    pattern.write_result(file_name=FILE_NAME, data=total_data)
    webbrowser.open(FILE_NAME)



