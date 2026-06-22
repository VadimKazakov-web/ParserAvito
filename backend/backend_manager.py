# -*- coding: utf-8 -*-
import subprocess
from threading import Thread
from backend.work_flow import WorkFlow
import queue
from backend.receiver import recv


def kill_process(pid: str) -> None:
    pid = str(pid)
    complete_process = subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, shell=True)
    if complete_process.returncode == 0:
        print(complete_process.stdout.decode(encoding='oem'))
    else:
        print(complete_process.stderr.decode(encoding='oem'))


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
        receiver_1 = Thread(target=self._receiver, daemon=True)
        receiver_1.start()
        while True:
            """
            Запуск основной работы программы: открытия страниц, объявлений, сбор информации
            """
            with WorkFlow(channel_put=self._channel_get) as work_flow:
                work_flow()
