# -*- coding: utf-8 -*-
import os
import shutil
import time
from tkinter import *
from settings import APP_TEMPORARY
from backend import connector
from tkinter_frontend.events import Events
from backend.events import EventsConnector


class WindowRoot:
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
        self.root.mainloop()

    def exit(self, *args, **kwargs):
        # отправляется событие в connector, который слушается в  BackendManager._receiver_for_main
        connector.put(Events.exit_event)
        # после закомментирования этого вызова, стали приходить данные в connector что было не всегда
        # перемещён в BackendManager._receiver_for_main
        # self.root.destroy()
        try:
            shutil.rmtree(APP_TEMPORARY)
        except FileNotFoundError:
            pass
        # этот вызов перемещён намеренно в BackendManager._receiver_for_main
        # программа завершается корректно только так
        # os._exit(0)

