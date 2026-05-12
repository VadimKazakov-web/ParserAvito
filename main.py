# -*- coding: utf-8 -*-
import multiprocessing
import os
from threading import Thread
import logging.handlers
from multiprocessing import Process
from backend.backend_manager import BackendManager
from tkinter_frontend.events import Events, InfoUpdateEvent
from tkinter_frontend.window_root.build import window as tk_window
from tkinter_frontend.build_tk import build_tk_interface
from utills.utils import logging_settings
from backend import connector
from backend.variables import Variables
from tkinter_frontend.utils import (create_progress, update_progress, update_info,
                                    update_time, update_version, create_install_prog_btn, new_flow_btn)

channel_backend = multiprocessing.JoinableQueue()


def _receiver():
    while True:
        data = connector.get()
        # print("data in main's _receiver: {}".format(data))
        if isinstance(data, Variables):
            channel_backend.put(data)
        if isinstance(data, InfoUpdateEvent):
            # print("InfoUpdateEvent data: {}".format(data.data))
            update_info(data.data)
        elif data == Events.push_stop_event:
            channel_backend.put(data)
        elif data == Events.new_flow_event:
            new_flow_btn()
        elif data == Events.exit_event:
            channel_backend.put(data)
            channel_backend.join()
        connector.task_done()


def main(*args, **kwargs):
    print("pid main proc: {}".format(os.getpid()))
    # настройка ведения журнала
    logging_settings(file_handler=False)
    logging.info("start program")

    # запуск слушателя данных из tkinter и процесса BackendManager
    receiver_t = Thread(target=_receiver, daemon=True)
    receiver_t.start()

    # запуск серверной части в отдельном процессе
    proc = Process(target=BackendManager, kwargs={
        # процесс будет получать данные из канала
        "channel_get": channel_backend,
        # процесс будет отправлять данные в канал
        "channel_put": connector,
    })
    proc.start()

    # создание всех элементов интерфейса tkinter
    build_tk_interface()
    # запуск главного цикла tkinter
    tk_window.start()
    proc.join()


if __name__ == '__main__':
    main()
