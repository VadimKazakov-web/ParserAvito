# -*- coding: utf-8 -*-
import logging
from update import Update
from tkinter_frontend.classes.label import Label
from tkinter_frontend.classes.button import Button
from tkinter_frontend import frame_2

label = Label(master=frame_2, text="", column=0, row=0)
label_instance = label.get_instance()
label_instance["width"] = 20
label.build()

button_custom = Button(master=frame_2, text="    проверить обновление   ", column=0, row=1)
button_custom.build()
button_custom.make_hover()
button_instance = button_custom.get_instance()
upd = Update()
button_instance.bind("<ButtonPress-1>", upd.check_update)
logging.info("{}: done".format(__name__))
