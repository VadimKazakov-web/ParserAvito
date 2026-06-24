# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.classes.label import LabelForUpdate
from tkinter_frontend.classes.button import ButtonForUpdate
from tkinter_frontend.window_root.frame_2.build import frame_2
from update.update_thread import CheckUpdateProgThread

"""
Создание кнопки для проверки обновления
"""

label = LabelForUpdate(master=frame_2, text="проверить обновление", column=0, row=0)
label_instance = label.get_instance()
label_instance["width"] = 33
label.build()

button_custom = ButtonForUpdate(master=frame_2, text="?", column=0, row=1)
button_custom.build()
button_custom.make_hover()
button_instance = button_custom.get_instance()
button_instance.bind("<ButtonPress-1>", func=CheckUpdateProgThread.start)
logging.info("{}: done".format(__name__))
