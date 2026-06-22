# -*- coding: utf-8 -*-
import os
import shutil
import time
from backend import Variables
from backend.events import EventsConnector
from settings import APP_TEMPORARY
from tkinter_frontend.events import ProgressData, Events
from update.update_classs import run_new_app


def recv(self) -> None:
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

        elif isinstance(data, ProgressData):
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
            try:
                shutil.rmtree(APP_TEMPORARY)
            except FileNotFoundError:
                pass
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

