# -*- coding: utf-8 -*-
import logging
import queue


class ClientMixin:
    """
    Класс для отправки данных в очередь
    """
    # очередь данных для бэкэнда
    channel_for_backend = queue.Queue()
    # очередь данных для интерфейса
    channel_for_tkinter = queue.Queue()

    @classmethod
    def post_data(cls, *args, **kwargs):
        data = kwargs.get("data")
        cls.channel_for_backend.put(data)

    @classmethod
    def post_data_tk(cls, *args, **kwargs):
        data = kwargs.get("data")
        cls.channel_for_tkinter.put(data)
