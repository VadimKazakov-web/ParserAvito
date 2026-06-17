# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.classes.frame import Frame
from tkinter_frontend.handlers.input_handlers import HandlersClass
from tkinter_frontend.window_root.build import ROOT
from backend import connector, Variables
from tkinter_frontend.events import Events

frame_custom = Frame(column=1, row=0, master=ROOT)
frame_custom.build()
frame = frame_custom.get_instance()
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=1)
frame.bind(Events.push_start_event, func=lambda _: HandlersClass.valid_all_vars(master=frame))
frame.bind(Events.post_var_event, func=lambda _: connector.put(Variables(HandlersClass.data)))
frame.bind(Events.push_stop_event, func=lambda _: connector.put(Events.push_stop_event))
logging.info("{}: done".format(__name__))
