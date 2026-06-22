# -*- coding: utf-8 -*-
import logging
from tkinter_frontend.events import Events
from tkinter_frontend.utils import ActiveInactiveButton
from tkinter_frontend.window_root.frame_1.frame_for_buttons.build import frame_for_buttons
from tkinter_frontend.classes.button import Button
from tkinter_frontend.window_root.frame_1.build import frame

"""
Создание кнопки Start
"""

button_custom = Button(master=frame_for_buttons, text="Start", column=0, row=0)
button_custom.build()
button_custom.make_hover()
button_instance = button_custom.get_instance()
active_inactive_start_button = ActiveInactiveButton(button_custom, button_instance,
                                                    lambda _: frame.event_generate(Events.push_start_event))
active_inactive_start_button.make_active_button()
# событие генерируется в tkinter_frontend.handlers.input_handlers.HandlersClass.valid_all_vars
button_instance.bind(Events.post_var_event, func=lambda _: active_inactive_start_button.make_inactive_button())
logging.info("{}: done".format(__name__))
