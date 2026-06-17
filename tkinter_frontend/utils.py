# -*- coding: utf-8 -*-
import _tkinter
from tkinter_frontend.classes.button import ButtonForUpdate
from update.update_thread import UpdateProgThread


def new_flow_btn(*args, **kwargs):
    from tkinter_frontend.window_root.frame_1.stop_button.build import active_inactive_stop_button
    from tkinter_frontend.window_root.frame_1.start_button.build import active_inactive_start_button
    active_inactive_stop_button.make_inactive_button()
    active_inactive_start_button.make_active_button()


def update_info(data):
    from tkinter_frontend.window_root.frame_1.frame_for_info.build import label_text_info
    label_text_info["text"] = data


def unbind_return(*args, **kwargs):
    event = args[0]
    widget = event.widget
    for elem in widget.winfo_children():
        elem.unbind("<Return>")


def update_progress(*args, **kwargs):
    from tkinter_frontend.window_root.frame_1.progress_bar.build import label_progress_origin, label_title_page_origin
    title, progr = kwargs.get("data")
    try:
        label_title_page_origin["text"] = title
        label_progress_origin["text"] = "обработано: {}".format(progr)
    except _tkinter.TclError:
        pass


def create_install_prog_btn(*args, **kwargs):
    from tkinter_frontend.window_root.frame_2.build import frame_2
    button_custom = ButtonForUpdate(master=frame_2, text="загрузить новую версию", column=0, row=2)
    button_custom.build()
    button_custom.make_hover()
    button_instance = button_custom.get_instance()
    button_instance.bind("<ButtonPress-1>", func=UpdateProgThread.start)


class ActiveInactiveButton:

    def __init__(self, button_custom, button_instance, callback):
        self.button_custom = button_custom
        self.button_instance = button_instance
        self.callback = callback

    def make_inactive_button(self, *args, **kwargs):
        self.button_instance["background"] = "#808080"
        self.button_instance["cursor"] = "arrow"
        self.button_instance.unbind("<ButtonPress-1>")
        self.button_custom.delete_hover()

    def make_active_button(self, *args, **kwargs):
        self.button_instance["background"] = "white"
        self.button_instance["cursor"] = "hand2"
        self.button_custom.make_hover()
        self.button_instance.bind("<ButtonPress-1>", func=self.callback)


