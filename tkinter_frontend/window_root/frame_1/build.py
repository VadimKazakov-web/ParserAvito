# -*- coding: utf-8 -*-
import logging
from objects import connector
from tkinter_frontend.classes.frame import Frame
from tkinter_frontend.window_root.build import window
from objects import client
from tkinter_frontend.handlers.input_handlers import HandlersClass
import functools
from tkinter_frontend.window_root.frame_1.utils import create_progress, update_progress, update_info

ROOT = window.get_root()
frame_custom = Frame(column=1, row=0, master=ROOT)
frame_custom.build()
frame = frame_custom.get_instance()
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=1)
frame.bind(connector.post_data_event, func=functools.partial(client.post_data, data=HandlersClass.data))
frame.bind(connector.create_progress_event, create_progress)
frame.bind(connector.update_progress_event, update_progress)
frame.bind(connector.update_info_event, update_info)

logging.info("{}: done".format(__name__))

