# -*- coding: utf-8 -*-
import logging
import queue


class ClientMixin:
    channel_for_variables = queue.Queue()
    channel_for_tkinter = queue.Queue()

    @classmethod
    def post_data(cls, *args, **kwargs):
        data = kwargs.get("data")
        cls.channel_for_variables.put(data)
        # logging.info("send data to backend:\n\t"
        #              "{data}".format(data=kwargs.get("data")))

    @classmethod
    def post_data_tk(cls, *args, **kwargs):
        data = kwargs.get("data")
        cls.channel_for_tkinter.put(data)
        logging.info("send data to tkinter:\n\t"
                     "{data}".format(data=kwargs.get("data")))

