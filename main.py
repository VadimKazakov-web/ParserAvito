# -*- coding: utf-8 -*-
import threading
import logging.handlers
from settings import *
from tkinter_frontend.window_root.build import window as tk_interface
from tkinter_frontend.build_tk import build_tk_interface
from parser_avito_manager.open_pages_manager import ParserAvitoManager

FORMAT = '[%(asctime)s] %(message)s'
formatter = logging.Formatter(FORMAT)
file_handler = True
if not file_handler:
    handler = logging.StreamHandler()
else:
    handler = logging.handlers.RotatingFileHandler(filename=LOG_DIR / LOG_FILE, maxBytes=6000, backupCount=4)
handler.setFormatter(formatter)
logging.root.setLevel(logging.INFO)
logging.root.handlers.clear()
logging.root.addHandler(handler)

logging.info("start program")
instance = ParserAvitoManager()
thread = threading.Thread(target=instance.start)
thread.start()
build_tk_interface()
tk_interface.start()
thread.join()
