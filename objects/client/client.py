# -*- coding: utf-8 -*-
import logging


class Client:

    def __init__(self, channel_for_variables):
        self.channel_for_variables = channel_for_variables

    def post_data(self, *args, **kwargs):
        data = kwargs.get("data")
        self.channel_for_variables.put(data)
        logging.info("{module}: done\n\tsend data to backend:\n\t"
                     "{data}".format(module=__name__, data=kwargs.get("data")))

