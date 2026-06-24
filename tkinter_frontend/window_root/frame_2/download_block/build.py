# -*- coding: utf-8 -*-
from tkinter_frontend.classes.button import ButtonForUpdate
from tkinter_frontend.window_root import frame_2
from update.update_thread import UpdateProgThread

button_custom = ButtonForUpdate(master=frame_2, text="загрузить", column=0, row=2)
button_custom.build()
button_custom.make_hover()
button_instance = button_custom.get_instance()
button_instance.bind("<ButtonPress-1>", func=UpdateProgThread.start)
