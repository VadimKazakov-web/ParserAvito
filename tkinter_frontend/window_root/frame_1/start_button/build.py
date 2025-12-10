# -*- coding: utf-8 -*-
import logging

from tkinter_frontend.window_root.frame_1.utils import ActiveInactiveButton
from tkinter_frontend.window_root.frame_1.frame_for_buttons.build import frame_for_buttons
from tkinter_frontend.classes.button import Button
from tkinter_frontend.objects import frame
from tkinter_frontend.handlers.input_handlers import HandlersClass
import functools

button_custom = Button(master=frame_for_buttons, text="Start", column=0, row=0)
button_custom.build()
button_custom.make_hover()
button_instance = button_custom.get_instance()
active_inactive_start_button = ActiveInactiveButton(button_custom, button_instance,
                                                    functools.partial(HandlersClass.valid_all_vars,
                                                                      widget=button_custom,
                                                                      master=frame))
active_inactive_start_button.make_active_button()
logging.info("{}: done".format(__name__))
