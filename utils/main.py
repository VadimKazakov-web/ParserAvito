from parser_avito_manager.open_pages_manager import ParserAvitoManager
import logging


def start_parser_instance(channel_for_variables, test=False):

    with ParserAvitoManager(channel_for_variables=channel_for_variables, test=test) as manager:
        manager.start()
