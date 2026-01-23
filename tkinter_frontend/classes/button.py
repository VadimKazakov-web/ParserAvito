# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter_frontend.classes import Base
from tkinter_frontend.classes.hover_effect import HoverEffectMixin


class Button(Base, HoverEffectMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = kwargs.get("text")
        self.instance = ttk.Label(master=self.master, text=self.text, font=Base.font,
                                  background=self.BACKGROUND_COLOR_BTN,
                                  foreground=self.FOREGROUND_COLOR_BTN,
                                  anchor="center", cursor="hand2", style="Button.TLabel")
        HoverEffectMixin.__init__(self, instance=self.instance, default_color=self.BACKGROUND_COLOR_BTN)

    def build(self):
        self.instance.grid(column=self.column, row=self.row, sticky=W)
        self.instance.grid_configure(ipadx=20, ipady=5)
        self.padding_configure()
