# -*- coding: utf-8 -*-
import logging


def build_tk_interface():
    """
    Построение всех элементов интерфейса tkinter
    """
    import tkinter_frontend.window_root.frame_0.build
    import tkinter_frontend.window_root.frame_1.build
    import tkinter_frontend.window_root.frame_1.get_link_block.build
    import tkinter_frontend.window_root.frame_1.get_filename_block.build
    import tkinter_frontend.window_root.frame_1.get_count_pages.build
    import tkinter_frontend.window_root.frame_1.frame_for_buttons.build
    import tkinter_frontend.window_root.frame_1.frame_for_buttons.start_button.build
    import tkinter_frontend.window_root.frame_1.frame_for_buttons.stop_button.build
    import tkinter_frontend.window_root.frame_1.progress_bar.build
    import tkinter_frontend.window_root.frame_2.build
    import tkinter_frontend.window_root.frame_2.update_block.build
    logging.info("{}: done".format(__name__))
