# -*- coding: utf-8 -*-
from objects import connector


def unbind_return(*args, **kwargs):
    event = args[0]
    widget = event.widget
    for elem in widget.winfo_children():
        elem.unbind("<Return>")


def create_progress(*args):
    import tkinter_frontend.window_root.frame_1.progress_bar.build


def update_progress(*args, **kwargs):
    from tkinter_frontend.window_root.frame_1.progress_bar.build import label_progress_origin, label_title_page_origin
    chunk = 55
    title = connector.get_title()
    progr = connector.get_progress()
    if len(title) >= chunk:
        title_chunk = title[0:chunk] + "\n" + title[chunk:]
    else:
        title_chunk = title
    label_title_page_origin["text"] = title_chunk
    label_progress_origin["text"] = progr


def update_info(*args, **kwargs):
    from tkinter_frontend.window_root.frame_1.frame_for_info.build import label_text_info
    label_text_info["text"] = connector.get_info()


def update_time(*args, **kwargs):
    from tkinter_frontend.window_root.frame_1.progress_bar.build import label_time_origin
    label_time_origin["text"] = connector.get_time()


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
        self.button_instance.bind("<ButtonPress-1>", self.callback)
