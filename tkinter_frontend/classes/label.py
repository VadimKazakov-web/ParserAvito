# -*- coding: utf-8 -*-
from tkinter import ttk, W
from tkinter_frontend.classes import Base


class Label(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = kwargs.get("text")
        self.instance = ttk.Label(master=self.master, text=self.text, font=Base.font,
                                  background=self.BACKGROUND_COLOR,
                                  foreground=self.FOREGROUND_COLOR,
                                  width=self.WIDTH_LABEL)

    def build(self):
        self.instance.grid(column=self.column, row=self.row, sticky=W)
        self.padding_configure()


class LabelForUpdate(Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance["font"] = Base.font_small


