# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.window_root.frame_1.build import frame
from tkinter_frontend.classes.button import Button
from tkinter_frontend.handlers.input_handlers import HandlersClass
import functools

button_custom = Button(master=frame, text="Start", column=0, row=6)
button_custom.build()
button_custom.make_hover()
button_instance = button_custom.get_instance()


button_instance.bind("<ButtonPress-1>", functools.partial(HandlersClass.valid_all_vars, widget=button_custom,
                                                          master=frame))
logging.info("{}: done".format(__name__))
