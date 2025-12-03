# -*- coding: utf-8 -*-
from objects import data_for_prog


def unbind_return(*args, **kwargs):
    event = args[0]
    widget = event.widget
    for elem in widget.winfo_children():
        elem.unbind("<Return>")


def create_progress(*args):
    import tkinter_frontend.window_root.frame_1.progress_bar.build


def update(*args):
    from tkinter_frontend.window_root.frame_1.progress_bar.build import label_origin, label_title_page_origin
    chunk = 55
    title = data_for_prog.get("page_title")
    if len(title) >= chunk:
        result = title[0:chunk] + "\n" + title[chunk:]
    else:
        result = title
    label_title_page_origin["text"] = result
    label_origin["text"] = data_for_prog.get("text")

