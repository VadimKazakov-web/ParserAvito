# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.classes.frame import Frame
from tkinter_frontend.classes.label import Label
from tkinter import ttk, font
from tkinter_frontend.window_root.frame_1.build import frame
from settings import FONT_SIZE

frame_custom = Frame(column=0, row=7, master=frame)
frame_custom.build()
frame_for_info = frame_custom.get_instance()
frame_for_info.grid_configure(padx=5, pady=5)
frame_for_info["padding"] = 0
frame_for_info["borderwidth"] = 3
frame_for_info["relief"] = "ridge"

font = font.Font()
font.configure(size=FONT_SIZE - 1)
color = "#FFFF00"

label_title = Label(master=frame_for_info, text="информация:", column=0, row=0)
label_title.build()
label_title_instance = label_title.get_instance()
label_title_instance["font"] = font
label_title_instance["foreground"] = color

label_info_block = Label(master=frame_for_info, text="", column=0, row=1)
label_info_block.build()
label_text_info = label_info_block.get_instance()
label_text_info["font"] = font
label_text_info["foreground"] = color
logging.info("{}: done".format(__name__))
