import traceback
from parser_avito_manager.open_pages_manager import ParserAvitoManager
import logging
from exceptions import BadInternetConnection


def start_parser_instance(channel_for_variables, data_for_progress, test=False):
    logging.info("start parser")

    while True:
        try:
            manager = ParserAvitoManager(channel_for_variables=channel_for_variables,
                                         data_for_progress=data_for_progress, test=test)
            manager.start()
        except BadInternetConnection:
            logging.warning("bad connections in avito.ru")
        except Exception as err:
            traceback.print_exception(err)
