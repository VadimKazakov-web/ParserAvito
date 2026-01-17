# -*- coding: utf-8 -*-
import threading
import logging.handlers
import functools
from settings import *
from tkinter_frontend.window_root.build import window as tk_interface
from tkinter_frontend.main import build_tk_interface
from utils.main import start_parser_instance

FORMAT = '[%(asctime)s] %(message)s'
formatter = logging.Formatter(FORMAT)
file_handler = False
if not file_handler:
    handler = logging.StreamHandler()
else:
    handler = logging.handlers.RotatingFileHandler(filename=LOG_DIR / LOG_FILE, maxBytes=6000, backupCount=4)
handler.setFormatter(formatter)
logging.root.setLevel(logging.INFO)
logging.root.handlers.clear()
logging.root.addHandler(handler)

logging.info("start program")
instance = functools.partial(start_parser_instance)
parser = threading.Thread(target=instance)
parser.start()
build_tk_interface()
tk_interface.start()
parser.join()
