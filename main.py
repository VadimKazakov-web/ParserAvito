# -*- coding: utf-8 -*-
import functools
import threading
import logging.handlers
from settings import PYINSTALLER_WORK_DIR
from tkinter_frontend.window_root.build import window as tk_interface
from tkinter_frontend.build_tk import build_tk_interface
from parser_avito_manager.backend_manager import ParserAvitoManager
from utills.utils import ControlPyinstallerWorkDir, logging_settings

logging_settings(file_handler=False)
logging.info("start program")

instance = ParserAvitoManager()
thread = threading.Thread(target=instance.start)
thread.start()

build_tk_interface()
tk_interface.start()

thread.join()
