# -*- coding: utf-8 -*-
import logging
from update.update_classs import Update
from tkinter_frontend.classes.label import Label, LabelForUpdate
from tkinter_frontend.classes.button import Button, ButtonForUpdate
from tkinter_frontend.window_root.frame_2.build import frame_2

label = LabelForUpdate(master=frame_2, text="", column=0, row=0)
label_instance = label.get_instance()
label_instance["width"] = 33
label.build()

button_custom = ButtonForUpdate(master=frame_2, text="проверить обновление\nпрограммы", column=0, row=1)
button_custom.build()
button_custom.make_hover()
button_instance = button_custom.get_instance()
button_instance.bind("<ButtonPress-1>", Update.check_update)
logging.info("{}: done".format(__name__))
