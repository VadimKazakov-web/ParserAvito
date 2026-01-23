# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.classes.frame import Frame
from tkinter_frontend import frame


frame_custom = Frame(column=0, row=6, master=frame)
frame_custom.build()
frame_for_options = frame_custom.get_instance()
frame_for_options["padding"] = (0, 10)
frame_for_options["borderwidth"] = 4


# эффект утопленности
# frame_for_options["relief"] = "sunken"
# эффект выступа
# frame_for_options["relief"] = "raised"
# простая рамка
# frame_for_options["relief"] = "solid"
# эффект объёма
# frame_for_options["relief"] = "ridge"

# frame_for_options["relief"] = "groove"


# frame.columnconfigure(1, weight=0)
# frame.columnconfigure(2, weight=1)
logging.info("{}: done".format(__name__))
