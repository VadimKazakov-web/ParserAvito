# -*- coding: utf-8 -*-
from tkinter_frontend.classes.label import Label
from tkinter_frontend.window_root import frame

label = Label(master=frame, text="Загрузка...", column=0, row=0)
label.build()
plug = label.get_instance()
