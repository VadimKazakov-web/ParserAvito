import time

from parser_avito_manager.open_pages_manager import ParserAvitoManager
import logging
from exceptions import BadInternetConnection
from tkinter_frontend.window_root.frame_1.start_button.utils import make_active_start_button


def start_parser_instance(channel_for_variables, data_for_progress, test=False):
    logging.info("start parser")
    try:
        manager = ParserAvitoManager(channel_for_variables=channel_for_variables,
                                data_for_progress=data_for_progress, test=test)
        while True:
            try:
                manager.start()
            except BadInternetConnection:
                logging.warning("bad connections in avito.ru")
                make_active_start_button()
            finally:
                make_active_start_button()
    except Exception as err:
        logging.info(err.__traceback__.stack)
