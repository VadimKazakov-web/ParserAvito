# -*- coding: utf-8 -*-
# import socket
# from dotenv import dotenv_values
# import json
import logging

from objects import config, channel_for_variables


class Client:

    def __init__(self):
        pass

    @staticmethod
    def post_data(*args, **kwargs):
        channel_for_variables.put(kwargs.get("data"))
        logging.info("{module}: done\n\tsend data to backend:\n\t"
                     "{data}".format(module=__name__, data=kwargs.get("data")))

