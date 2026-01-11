# -*- coding: utf-8 -*-
import logging
import queue


class ClientMixin:
    channel_for_variables = queue.Queue()

    @classmethod
    def post_data(cls, *args, **kwargs):
        data = kwargs.get("data")
        cls.channel_for_variables.put(data)
        logging.info("{module}: done\n\tsend data to backend:\n\t"
                     "{data}".format(module=__name__, data=kwargs.get("data")))

