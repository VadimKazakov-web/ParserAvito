# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter_frontend.classes import Base


class Frame(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = ttk.Frame(master=self.master, padding="20 50 20 50")

    def build(self):
        self.instance.grid(column=self.column, row=self.row, sticky=W + E + N + S)
