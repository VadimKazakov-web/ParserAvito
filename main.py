# -*- coding: utf-8 -*-
import os
from threading import Thread
import logging.handlers
from backend.backend_manager import BackendManager
from tkinter_frontend.window_root.build import window as tk_window
from tkinter_frontend.build_tk import build_tk_interface
from utills.utils import logging_settings
from backend import connector
PROCESS_PID = os.getpid()


def main(*args, **kwargs):
    print("process pid: {}".format(PROCESS_PID))
    # настройка ведения журнала
    logging_settings(file_handler=False)
    logging.info("start program")

    # запуск серверной части в отдельном потоке
    thread = Thread(target=BackendManager, kwargs={
        # поток будет получать данные из канала
        "channel_get": connector,
    })
    thread.start()

    # создание всех элементов интерфейса tkinter
    build_tk_interface()
    # запуск главного цикла tkinter
    tk_window.start()
    thread.join()


if __name__ == '__main__':
    main()
