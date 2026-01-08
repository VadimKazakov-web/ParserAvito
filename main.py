# -*- coding: utf-8 -*-
import os
import threading
import logging
import logging.handlers
import functools
from pathlib import Path

from tkinter_frontend.window_root.build import window as tk_interface
from objects import channel_for_variables
from tkinter_frontend.main import build_tk_interface
from utils.main import start_parser_instance

base_dir = Path(os.getcwd()) / Path("ParserAvitoOutput")
log_dir = base_dir / Path("log")

FORMAT = '[%(asctime)s] %(message)s'
formatter = logging.Formatter(FORMAT)
# handler = logging.StreamHandler()
try:
    handler = logging.handlers.RotatingFileHandler(filename=log_dir / Path("logbook.log"), maxBytes=6000, backupCount=4)
except FileNotFoundError:
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(filename=log_dir / Path("logbook.log"))
handler.setFormatter(formatter)
logging.root.setLevel(logging.INFO)
logging.root.handlers.clear()
logging.root.addHandler(handler)

logging.info("start program")
instance = functools.partial(start_parser_instance, channel_for_variables, base_dir)
parser = threading.Thread(target=instance)
parser.start()
build_tk_interface()
tk_interface.start()
parser.join()




