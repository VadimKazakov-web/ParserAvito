# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import Entry as EntryStock
from tkinter_frontend.classes import Base
from tkinter_frontend.classes.hover_effect import HoverEffectMixin


class Entry(Base, HoverEffectMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = StringVar()
        self.instance = EntryStock(master=self.master, font=Base.font,
                                   background=self.BACKGROUND_COLOR_ENTRY,
                                   foreground=self.FOREGROUND_COLOR_ENTRY,
                                   cursor="hand2",
                                   textvariable=self.text,
                                   width=self.WIDTH_LABEL)
        HoverEffectMixin.__init__(self, instance=self.instance, default_color=self.BACKGROUND_COLOR_ENTRY)


    def build(self):
        self.instance.grid(column=self.column, row=self.row, sticky=W)
        self.padding_configure()
        return self.text

    def get_textvariable(self):
        return self.text

    def get_instance(self):
        return self.instance
