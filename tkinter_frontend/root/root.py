# -*- coding: utf-8 -*-
import time
from tkinter import *
from backend import connector, Variables
from tkinter_frontend.events import Events
from tkinter_frontend.handlers.input_handlers import HandlersClass
from tkinter_frontend.utils import create_download_prog_btn


class WindowRoot:

    """
    Класс для создания главного окна tkinter
    """

    def __init__(self, name):
        self.name = name
        self.root = Tk()
        self.root.title(self.name)
        self.setup_weight()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

    def get_root(self):
        return self.root

    def setup_weight(self):
        # настройка весности сетки
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)

    def start(self):
        self.root.bind(Events.push_start_event, func=HandlersClass.valid_all_vars)
        self.root.bind(Events.post_var_event, func=lambda _: connector.put(Variables(HandlersClass.data)))
        self.root.bind(Events.push_stop_event, func=lambda _: connector.put(Events.push_stop_event))
        self.root.bind(Events.create_download_btn_event, func=create_download_prog_btn)
        self.root.mainloop()

    def exit(self, *args, **kwargs):
        from tkinter_frontend.window_root import frame
        # отправляется событие в connector, который слушается в  BackendManager._receiver_for_main
        connector.put(Events.exit_event)
