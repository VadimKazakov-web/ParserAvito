import logging
from preparation_links_for_pages import PreparationLinksForPages
from open_pages_manager import OpenPagesManager
from result_in_html import ResultInHtml

FORMAT = '[%(asctime)s]%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

PAGES = 2
URL = 'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc'
FILE_NAME = 'result.html'

prep_links_instance = PreparationLinksForPages(url=URL, pages=PAGES)
prep_links_instance.start()
links_pages = prep_links_instance.result

with OpenPagesManager(links=links_pages, test=True) as manager:
    manager.start()
    total_data = manager.total_data
    logging.info("\n\n")
    logging.info("+++++++ total data: {}".format(total_data))
    logging.info("+++++++ length total data: {}".format(len(total_data)))

    pattern = ResultInHtml()
    pattern.write_result(file_name=FILE_NAME, data=total_data)



