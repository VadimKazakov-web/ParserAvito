# -*- coding: utf-8 -*-
import logging

from tkinter_frontend.classes.frame import Frame
from tkinter_frontend.window_root.build import ROOT
from tkinter_frontend.client.client import Client
from tkinter_frontend.handlers.input_handlers import HandlersClass
import functools


frame_custom = Frame(column=1, row=0, master=ROOT)
frame_custom.build()
frame = frame_custom.get_instance()
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=1)
client = Client()
frame.bind("<<PostData>>", func=functools.partial(client.post_data, data=HandlersClass.data))
logging.info("{}: done".format(__name__))

