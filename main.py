# -*- coding: utf-8 -*-
import threading
import logging
import functools
from tkinter_frontend.window_root.build import window as tk_interface
from objects import channel_for_variables, progress
from tkinter_frontend.main import build_tk_interface
from utils.main import start_parser_instance


FORMAT = '[%(asctime)s] %(message)s'
formatter = logging.Formatter(FORMAT)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.setLevel(logging.INFO)
logging.root.handlers.clear()
logging.root.addHandler(handler)

logging.info("start program")
instance = functools.partial(start_parser_instance, channel_for_variables, progress)
parser = threading.Thread(target=instance, daemon=True)
parser.start()
build_tk_interface()
tk_interface.start()
parser.join()



