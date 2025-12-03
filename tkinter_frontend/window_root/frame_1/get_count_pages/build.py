# -*- coding: utf-8 -*-
import logging

from tkinter_frontend.window_root.frame_1.build import frame
from tkinter_frontend.classes.label import Label
from tkinter_frontend.classes.entry import Entry
from tkinter_frontend.classes.label_icon import LabelIcon
import functools
from tkinter_frontend.handlers.input_handlers import HandlersClass

label = Label(master=frame, text="Введите количество страниц для сканирования", column=0, row=4)
label.build()

entry_custom = Entry(master=frame, column=0, row=5, name="pages_entry")
entry_custom.build()
entry_custom.make_hover()
entry = entry_custom.get_instance()
textvariable = entry_custom.get_textvariable()

label_icon = LabelIcon(column=1, row=5, master=frame, text="❓")
label_icon.build()

entry.bind("<Return>", func=functools.partial(HandlersClass.count_page_handler,
                                              entry=textvariable, label=label.get_instance(),
                                              icon=label_icon))
logging.info("{}: done".format(__name__))


