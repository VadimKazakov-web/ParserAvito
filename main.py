# -*- coding: utf-8 -*-
from threading import Thread
import logging.handlers
from multiprocessing import Process
from backend.backend_manager import BackendManager
from tkinter_frontend.events import Events, InfoUpdateEvent
from tkinter_frontend.window_root.build import window as tk_window
from tkinter_frontend.build_tk import build_tk_interface
from utills.utils import logging_settings
from backend import connector, channel_for_main_proc
from backend.variables import Variables
from tkinter_frontend.utils import (create_progress, update_progress, update_info,
                                    update_time, update_version, create_install_prog_btn, new_flow_btn)


def _receiver():
    while True:
        data = channel_for_main_proc.get()
        if data == Events.new_flow_event:
            new_flow_btn()
        elif isinstance(data, InfoUpdateEvent):
            Variables.set_info(data.data)
            update_info()


def main(*args, **kwargs):
    # настройка ведения журнала
    logging_settings(file_handler=False)
    logging.info("start program")

    # запуск слушателя данных из процесса серверной части
    receiver_t = Thread(target=_receiver, daemon=True)
    receiver_t.start()

    # запуск серверной части в отдельном процессе
    backend_manager = BackendManager()
    proc = Process(target=backend_manager, kwargs={
        "channel": connector,
        "channel_for_main_proc": channel_for_main_proc,
    })
    proc.start()

    # создание всех элементов интерфейса tkinter
    build_tk_interface()
    # запуск главного цикла tkinter
    tk_window.start()
    proc.join()


if __name__ == '__main__':
    main()
