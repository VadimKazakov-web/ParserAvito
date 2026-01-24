# -*- coding: utf-8 -*-
from tkinter import W
from tkinter import ttk
from tkinter_frontend.classes import Base


class LabelIcon(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = kwargs.get("text")
        self.style_default = ttk.Style()
        self.style_default.configure(style="IconUnchecked.TLabel", foreground="#FF0000")
        self.style_verified = ttk.Style()
        self.style_verified.configure(style="IconValid.TLabel", foreground="#00FF00")
        self.instance = ttk.Label(master=self.master, text=self.text, font=Base.font, style="IconUnchecked.TLabel",
                                  background=self.BACKGROUND_COLOR)

    def build(self):
        self.instance.grid(column=self.column, row=self.row, sticky=W)
        self.padding_configure()

    def make_verified(self):
        self.instance["style"] = "IconValid.TLabel"
        self.instance["text"] = "✔"
        return self.instance

    def make_unchecked(self):
        self.instance["style"] = "IconUnchecked.TLabel"
        self.instance["text"] = "❓"
        return self.instance
