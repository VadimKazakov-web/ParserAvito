# -*- coding: utf-8 -*-
import os
import subprocess
import time
from threading import Thread
from backend import (Variables, DataBaseMixin, CreateDriverMixin)
from backend.events import EventsConnector
from tkinter_frontend.events import Events, ProgressUpdateEvent
from backend.work_flow import WorkFlow
import queue
from update.update_classs import run_new_app


def kill_process(pid: str) -> None:
    pid = str(pid)
    complete_process = subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, shell=True)
    if complete_process.returncode == 0:
        print(complete_process.stdout.decode(encoding='oem'))
    else:
        print(complete_process.stderr.decode(encoding='oem'))


class BackendManager(DataBaseMixin, CreateDriverMixin):

    def __init__(self, *args, **kwargs):
        # канал получения данных из tkinter в поток BackendManager
        self._channel_get: queue.Queue = kwargs.get("channel_get")
        self.data = None

    def __str__(self) -> str:
        return "BackendManager"

    def _receiver_for_main(self) -> None:
        from tkinter_frontend.utils import new_flow_btn, update_progress
        """
        Метод получает данные из потока main
        """
        while True:
            data = self._channel_get.get()
            if isinstance(data, Variables):
                """
                Получение ссылки, названия файла и кол-во страниц для сканирования из интерфейса tkinter
                """
                print("data from connector: {}".format(data.variables))
                self.data = data
                EventsConnector.variables_put(data)

            elif isinstance(data, ProgressUpdateEvent):
                """
                Отправка данных прогресса в интерфейс tkinter: заголовок страницы и кол-во обработанных объявлений
                """
                update_progress(data=(data.text, data.num))

            elif data == Events.push_stop_event:
                """
                Нажатие кнопки "stop"
                """
                print("data from connector: {}".format(data))
                new_flow_btn()
                EventsConnector.push_stop()

            elif data == Events.window_close_event:
                """
                Закрытие окна браузера
                """
                print("data from connector: {}".format(data))
                new_flow_btn()

            elif data == Events.exit_event:
                """
                Закрытие главного окна программы
                """
                print("data from connector: {}".format(data))
                if self.data:
                    EventsConnector.push_exit()
                    EventsConnector.work_wait()
                # программа завершается корректно только так
                os._exit(0)

            elif data == Events.start_again_event:
                print("data from connector: {}".format(data))
                EventsConnector.variables_put(self.data)

            elif data == Events.exit_after_update_event:
                """
                Действия, которые происходят после обновления программы: запуск новой программы
                с помощью утилиты windows schtasks /run, и закрытия старой программы
                """
                print("data from connector: {}".format(data))
                if self.data:
                    EventsConnector.push_update()
                    EventsConnector.work_wait()
                run_new_app()
                time.sleep(1)
                os._exit(0)

    def __call__(self, *args, **kwargs) -> None:
        """
        Запуск слушателя событий из канала в отдельном потоке, которые приходят из интерфейса tkinter
        """
        receiver_1 = Thread(target=self._receiver_for_main, daemon=True)
        receiver_1.start()
        while True:
            """
            Запуск основной работы программы: открытия страниц, объявлений, сбор информации
            """
            with WorkFlow(channel_put=self._channel_get) as work_flow:
                work_flow()
