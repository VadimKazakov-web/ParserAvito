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
    title = data_for_prog.get(key="page_title")
    progress = data_for_prog.get(key="text")
    if len(title) >= chunk:
        title_chunk = title[0:chunk] + "\n" + title[chunk:]
    else:
        title_chunk = title
    label_title_page_origin["text"] = title_chunk
    label_origin["text"] = progress

