import traceback
from parser_avito_manager.open_pages_manager import ParserAvitoManager
import logging
from exceptions import BadInternetConnection, PushExit


def start_parser_instance(base_dir, test=False):
    logging.info("start parser")

    while True:
        try:
            manager = ParserAvitoManager(base_dir=base_dir,
                                         test=test)
            manager.start()
        except BadInternetConnection:
            logging.warning("bad connections in avito.ru")
        except PushExit as err:
            logging.info(err)
            break
        except Exception as err:
            traceback.print_exception(err)
