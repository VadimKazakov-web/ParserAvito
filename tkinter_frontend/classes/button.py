# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter_frontend.classes import Base
from tkinter_frontend.classes.hover_effect import HoverEffectMixin


class Button(Base, HoverEffectMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super(Base, self).__init__()
        self.text = kwargs.get("text")
        self.instance = ttk.Label(master=self.master, text=self.text, font=Base.font,
                                  background=self.config.get("FOREGROUND_COLOR", "white"),
                                  foreground="#000000",
                                  anchor="center", cursor="hand2", style="Button.TLabel")

    def build(self):
        self.instance.grid(column=self.column, row=self.row, sticky=W)
        self.instance.grid_configure(ipadx=20, ipady=5)
        self.padding_configure()
