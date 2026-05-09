# -*- coding: utf-8 -*-
import os
import shutil
import time
from tkinter import *
from objects import connector
from settings import APP_TEMPORARY


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
        connector.post_data(data="exit")
        self.root.destroy()
        time.sleep(3)
        shutil.rmtree(APP_TEMPORARY)
        # программа завершается корректно только так
        os._exit(0)

