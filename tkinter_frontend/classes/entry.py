# -*- coding: utf-8 -*-
from tkinter import StringVar, W, E
from tkinter import Entry as EntryStock
from tkinter_frontend.classes.base import Base
from tkinter_frontend.classes.hover_effect import HoverEffectMixin


class Entry(Base, HoverEffectMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = StringVar()
        self.instance = EntryStock(master=self.master, font=self.font,
                                   background=self.BACKGROUND_COLOR_ENTRY,
                                   foreground=self.FOREGROUND_COLOR_ENTRY,
                                   cursor="hand2",
                                   textvariable=self.text,
                                   width=self.WIDTH_LABEL)
        super(Base, self).__init__(self, instance=self.instance)

    def build(self):
        self.instance.grid(column=self.column, row=self.row, sticky=W + E)
        self.padding_configure()

    def get_textvariable(self):
        return self.text

    def get_instance(self):
        return self.instance
