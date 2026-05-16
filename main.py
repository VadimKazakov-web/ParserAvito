# -*- coding: utf-8 -*-
import os
from threading import Thread
import logging.handlers
from backend.backend_manager import BackendManager
from tkinter_frontend.window_root.build import window as tk_window
from tkinter_frontend.build_tk import build_tk_interface
from utills.utils import logging_settings
from backend import connector


def main(*args, **kwargs):
    print("process pid: {}".format(os.getpid()))
    # настройка ведения журнала
    logging_settings(file_handler=False)
    logging.info("start program")

    # запуск серверной части в отдельном процессе
    thread = Thread(target=BackendManager, kwargs={
        # процесс будет получать данные из канала
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
