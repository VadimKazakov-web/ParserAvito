# -*- coding: utf-8 -*-
import logging
from objects import connector
from tkinter_frontend.utils import ActiveInactiveButton, CheckUpdateProgThread
from tkinter_frontend.classes.label import Label, LabelForUpdate
from tkinter_frontend.classes.button import Button, ButtonForUpdate
from tkinter_frontend.window_root.frame_2.build import frame_2

label = LabelForUpdate(master=frame_2, text="", column=0, row=0)
label_instance = label.get_instance()
label_instance["width"] = 33
label.build()

button_custom = ButtonForUpdate(master=frame_2, text="проверить обновление", column=0, row=1)
button_custom.build()
button_custom.make_hover()
button_instance = button_custom.get_instance()
logging.info("{}: done".format(__name__))

act_inact_button = ActiveInactiveButton(button_custom, button_instance, CheckUpdateProgThread.start)
act_inact_button.make_active_button()

connector.set_callbacks_for_start_prog(act_inact_button.make_inactive_button)
connector.set_callbacks_for_stop_prog(act_inact_button.make_active_button)
