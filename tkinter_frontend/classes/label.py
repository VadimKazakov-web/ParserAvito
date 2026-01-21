# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter_frontend.classes import Base


class Label(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = kwargs.get("text")
        self.instance = ttk.Label(master=self.master, text=self.text, font=Base.font,
                                  background=self.config.get("BACKGROUND_COLOR", "blue"),
                                  foreground=self.config.get("FOREGROUND_COLOR", "white"),
                                  width=int(self.config.get("WIDTH_LABEL", 50)))

    def build(self):
        self.instance.grid(column=self.column, row=self.row, sticky=W)
        self.padding_configure()
