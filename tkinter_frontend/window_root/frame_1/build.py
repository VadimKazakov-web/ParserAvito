# -*- coding: utf-8 -*-
import logging
from objects import connector
from tkinter_frontend.classes.frame import Frame
from tkinter_frontend.handlers.input_handlers import HandlersClass
from tkinter_frontend.window_root.build import ROOT, window
from tkinter_frontend.utils import (create_progress, update_progress, update_info,
                                    update_time, update_version, create_install_prog_btn)
from tkinter_frontend.utils import new_flow_btn
from backend import connector
from tkinter_frontend.events import Events

frame_custom = Frame(column=1, row=0, master=ROOT)
frame_custom.build()
frame = frame_custom.get_instance()
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=1)
frame.bind(Events.push_start_event, func=lambda _: HandlersClass.valid_all_vars(master=frame))
frame.bind(Events.post_var_event, func=lambda _: connector.put(HandlersClass.data))
frame.bind(Events.push_stop_event, func=lambda _: connector.put(Events.push_stop_event))
# frame.bind(Events.new_flow_event, func=lambda _: new_flow_btn)
# frame.bind(Events.info_update_event, func=lambda _: update_info)

# frame.bind(connector.create_progress_event, create_progress)
# frame.bind(connector.update_progress_event, update_progress)
# frame.bind(connector.update_time_event, update_time)
# frame.bind(connector.update_version_event, update_version)
# frame.bind(connector.create_install_prog_event, create_install_prog_btn)
# frame.bind(connector.exit_event, window.exit)
#
# connector.add_widget(frame)

logging.info("{}: done".format(__name__))
