# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.classes.label import Label
from tkinter_frontend.objects import frame


label_title_page = Label(master=frame, text="...", column=0, row=9)
label_title_page_origin = label_title_page.get_instance()
label_title_page_origin['anchor'] = "w"
label_title_page.build()

label = Label(master=frame, text="...", column=0, row=10)
label_origin = label.get_instance()
label_origin['anchor'] = "w"
label.build()
logging.info("{}: done".format(__name__))
