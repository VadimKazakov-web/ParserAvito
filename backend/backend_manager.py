# -*- coding: utf-8 -*-
import subprocess
from threading import Thread

from backend import Variables
from backend.events import EventsConnector
from backend.work_flow import WorkFlow
import queue
from backend.receiver import recv


class BackendManager:

    def __init__(self, *args, **kwargs):
        # канал получения данных из tkinter в поток BackendManager
        self._channel_get: queue.Queue = kwargs.get("channel_get")
        self.data = None

    def __str__(self) -> str:
        return "BackendManager"

    def _receiver(self) -> None:
        recv(self)

    def __call__(self, *args, **kwargs) -> None:
        """
        Запуск слушателя событий из канала в отдельном потоке, которые приходят из интерфейса tkinter
        """
        receiver = Thread(target=self._receiver, daemon=True)
        receiver.start()
        while True:
            """
            Запуск основной работы программы: открытия страниц, объявлений, сбор информации
            """
            print("-" * 10, "waiting for the start", "-" * 10)
            self.data: Variables = EventsConnector.variables_wait()
            with WorkFlow(data=self.data, channel_put=self._channel_get) as work_flow:
                work_flow()
