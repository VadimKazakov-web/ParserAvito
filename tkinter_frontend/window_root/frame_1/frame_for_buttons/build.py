# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.classes.frame import Frame
from tkinter_frontend.window_root.frame_1.build import frame

"""
Создание фрейма для кнопок start/stop
"""

frame_custom = Frame(column=0, row=8, master=frame)
frame_custom.build()
frame_for_buttons = frame_custom.get_instance()
frame_for_buttons["padding"] = (0, 10)
logging.info("{}: done".format(__name__))
