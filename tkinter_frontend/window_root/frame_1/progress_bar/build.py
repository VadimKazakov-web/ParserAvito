# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.classes.label import Label
from tkinter_frontend.window_root.frame_1.build import frame

label_title = Label(master=frame, text="...", column=0, row=9)
label_title_page_origin = label_title.get_instance()
label_title_page_origin['anchor'] = "w"
label_title.build()

label = Label(master=frame, text="...", column=0, row=10)
label_progress_origin = label.get_instance()
label_progress_origin['anchor'] = "w"
label.build()

label_time = Label(master=frame, text="время выполнения: ", column=0, row=11)
label_time_origin = label_time.get_instance()
label_time_origin['anchor'] = "w"
label_time.build()
logging.info("{}: done".format(__name__))
