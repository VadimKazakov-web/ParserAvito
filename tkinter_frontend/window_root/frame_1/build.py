# -*- coding: utf-8 -*-
import logging

from objects import channel_for_variables
from tkinter_frontend.classes.frame import Frame
from tkinter_frontend.window_root.build import window
from tkinter_frontend.client.client import Client
from tkinter_frontend.handlers.input_handlers import HandlersClass
import functools
from tkinter_frontend.window_root.frame_1.utils import unbind_return, create_progress, update

ROOT = window.get_root()
frame_custom = Frame(column=1, row=0, master=ROOT)
frame_custom.build()
frame = frame_custom.get_instance()
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=1)
client = Client(channel_for_variables)
frame.bind("<<PostData>>", func=functools.partial(client.post_data, data=HandlersClass.data))
frame.bind("<<UnbindReturn>>", unbind_return)
frame.bind("<<CreateProgress>>", create_progress)
frame.bind("<<UpdateProgress>>", update)
logging.info("{}: done".format(__name__))

