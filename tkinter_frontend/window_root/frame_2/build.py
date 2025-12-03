# -*- coding: utf-8 -*-
import logging

from tkinter_frontend.classes.frame import Frame
from tkinter_frontend.window_root.build import window

ROOT = window.get_root()
frame_custom = Frame(column=2, row=0, master=ROOT)
frame_custom.build()
logging.info("{}: done".format(__name__))
