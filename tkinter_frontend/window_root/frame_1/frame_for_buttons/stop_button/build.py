# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.window_root.frame_1.frame_for_buttons.build import frame_for_buttons
from tkinter_frontend.classes.button import Button
from tkinter_frontend.events import Events
from tkinter_frontend.utils import ActiveInactiveButton
from tkinter_frontend.window_root.build import ROOT

"""
Создание кнопки Stop
"""

button_custom = Button(master=frame_for_buttons, text="Stop", column=1, row=0)
button_custom.build()
button_instance = button_custom.get_instance()
active_inactive_stop_button = ActiveInactiveButton(button_custom, button_instance,
                                                   lambda _: ROOT.event_generate(Events.push_stop_event))
active_inactive_stop_button.make_inactive_button()
# событие генерируется в tkinter_frontend.handlers.input_handlers.HandlersClass.valid_all_vars
button_instance.bind(Events.post_var_event_btn, func=active_inactive_stop_button.make_active_button)
logging.info("{}: done".format(__name__))
