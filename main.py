import logging
from preparation_links_for_pages import PreparationLinksForPages
from open_pages_manager import OpenPagesManager


FORMAT = '[%(asctime)s]%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

PAGES = 1
URL = 'https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc'

prep_links_instance = PreparationLinksForPages(url=URL, pages=PAGES)
prep_links_instance.start()
links_pages = prep_links_instance.result

with OpenPagesManager(links=links_pages) as manager:
    manager.start()
    total_data = manager.total_data
    logging.info("\n\n")
    logging.info("+++++++ total data: {}".format(total_data))
    logging.info("+++++++ length total data: {}".format(len(total_data)))


