# -*- coding: utf-8 -*-
import logging


def build_tk_interface():
    import tkinter_frontend.window_root.frame_0.build
    import tkinter_frontend.window_root.frame_1.get_link_block.build
    import tkinter_frontend.window_root.frame_1.get_filename_block.build
    import tkinter_frontend.window_root.frame_1.get_count_pages.build
    import tkinter_frontend.window_root.frame_1.frame_for_options.build
    import tkinter_frontend.window_root.frame_1.frame_for_options.radio_buttons.build
    import tkinter_frontend.window_root.frame_1.start_button.build
    import tkinter_frontend.window_root.frame_2.build
    logging.info("{}: done".format(__name__))
