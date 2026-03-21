# -*- coding: utf-8 -*-
import threading
import logging.handlers
from tkinter_frontend.window_root.build import window as tk_window
from tkinter_frontend.build_tk import build_tk_interface
from parser_avito_manager.backend_manager import ParserAvitoManager
from utills.utils import logging_settings

logging_settings(file_handler=False)
logging.info("start program")

instance = ParserAvitoManager()
thread = threading.Thread(target=instance.start)
thread.start()

build_tk_interface()
tk_window.start()

thread.join()
