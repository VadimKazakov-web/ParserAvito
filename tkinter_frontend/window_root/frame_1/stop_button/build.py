# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.window_root.frame_1.frame_for_buttons.build import frame_for_buttons
from tkinter_frontend.classes.button import Button
from tkinter_frontend.window_root.frame_1.utils import ActiveInactiveButton
from objects import client
import functools

button_custom = Button(master=frame_for_buttons, text="Stop", column=1, row=0)
button_custom.build()
button_instance = button_custom.get_instance()
active_inactive_stop_button = ActiveInactiveButton(button_custom, button_instance, functools.partial(client.post_data, data="push_stop_button"))
active_inactive_stop_button.make_inactive_button()
logging.info("{}: done".format(__name__))
