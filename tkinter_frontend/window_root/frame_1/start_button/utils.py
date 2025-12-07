from tkinter_frontend.handlers.input_handlers import HandlersClass
from tkinter_frontend.window_root.frame_1.start_button.build import button_custom, button_instance
import functools


def make_inactive_start_button():
    button_instance["background"] = "#808080"
    button_instance["cursor"] = "arrow"
    button_instance.unbind("<ButtonPress-1>")
    button_custom.delete_hover()


def make_active_start_button():
    from tkinter_frontend.window_root.frame_1.build import frame
    button_instance["background"] = "white"
    button_instance["cursor"] = "hand2"
    button_custom.make_hover()
    button_instance.bind("<ButtonPress-1>", functools.partial(HandlersClass.valid_all_vars, widget=button_custom,
                                                              master=frame))

