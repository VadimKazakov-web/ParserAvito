# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import Entry as EntryStock
from tkinter_frontend.classes.base import Base
from tkinter_frontend.classes.hover_effect import HoverEffectMixin


class Entry(Base, HoverEffectMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super(Base, self).__init__()
        self.text = StringVar()
        self.instance = EntryStock(master=self.master, font=Base.font,
                                   background="#FFFFFF",
                                   foreground="#000000",
                                   cursor="hand2",
                                   textvariable=self.text,
                                   width=int(self.config.get("WIDTH_LABEL", 50)))

    def build(self):
        self.instance.grid(column=self.column, row=self.row, sticky=W)
        self.padding_configure()
        return self.text

    def get_textvariable(self):
        return self.text

    def get_instance(self):
        return self.instance
