# -*- coding: utf-8 -*-
import logging

from objects import connector
from tkinter_frontend.classes.frame import Frame, FrameForUpdate
from tkinter_frontend.utils import update_version, create_install_prog_btn
from tkinter_frontend.window_root.build import window

ROOT = window.get_root()
frame_custom = FrameForUpdate(column=2, row=0, master=ROOT)
frame_2 = frame_custom.get_instance()
frame_custom.build()
logging.info("{}: done".format(__name__))
