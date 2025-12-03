from parser_avito_manager.open_pages_manager import ParserAvitoManager
import logging


def start_parser_instance(channel_for_variables, data_for_progress, test=False):
    logging.info("start parser")
    try:
        with ParserAvitoManager(channel_for_variables=channel_for_variables,
                                data_for_progress=data_for_progress, test=test) as manager:
            manager.start()
    except Exception as err:
        logging.info(err.__traceback__.stack)
