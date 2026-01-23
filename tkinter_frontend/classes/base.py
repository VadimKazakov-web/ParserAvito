# -*- coding: utf-8 -*-
from tkinter_frontend.classes import ConfigClass
from tkinter import *
from tkinter import ttk, font


class Base(ConfigClass):
    font = None
    style_frame = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.column = kwargs.get("column")
        self.row = kwargs.get("row")
        self.master = kwargs.get("master")
        self.instance = None
        if not Base.font:
            Base.font = font.Font(family='TkDefaultFont', name='default', size=self.FONT_SIZE)
        if not Base.style_frame:
            Base.style_frame = ttk.Style().configure(style='TFrame', background=self.BACKGROUND_COLOR)

    def get_instance(self):
        return self.instance

    def padding_configure(self):
        self.instance.grid_configure(padx=5, pady=5)
