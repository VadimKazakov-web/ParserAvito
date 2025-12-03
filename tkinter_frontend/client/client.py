# -*- coding: utf-8 -*-
import logging
from objects import config


class Client:

    def __init__(self, channel_for_variables):
        self.channel_for_variables = channel_for_variables

    def post_data(self, *args, **kwargs):
        widget = args[0].widget
        data = kwargs.get("data")
        data["widget_tk"] = widget
        self.channel_for_variables.put(data)
        logging.info("{module}: done\n\tsend data to backend:\n\t"
                     "{data}".format(module=__name__, data=kwargs.get("data")))

