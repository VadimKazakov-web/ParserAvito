# -*- coding: utf-8 -*-
import functools
import threading
import logging.handlers
from settings import LOG_DIR, LOG_FILE, PYINSTALLER_WORK_DIR, BASE_DIR
from tkinter_frontend.window_root.build import window as tk_interface
from tkinter_frontend.build_tk import build_tk_interface
from parser_avito_manager.backend_manager import ParserAvitoManager
from update.utills.utills import ControlPyinstallerWorkDir

FORMAT = '[%(asctime)s] %(message)s'
formatter = logging.Formatter(FORMAT)
file_handler = False
if not file_handler:
    handler = logging.StreamHandler()
else:
    handler = logging.handlers.RotatingFileHandler(filename=LOG_DIR / LOG_FILE, maxBytes=6000, backupCount=5)
handler.setFormatter(formatter)
logging.root.setLevel(logging.INFO)
logging.root.handlers.clear()
logging.root.addHandler(handler)

logging.info("start program")

# instance = ParserAvitoManager()
# thread = threading.Thread(target=instance.start)
# thread.start()

thread_control_work_dir = threading.Thread(target=functools.partial(
    ControlPyinstallerWorkDir.control_pyinstaller_work_dir, path=PYINSTALLER_WORK_DIR, desktop=BASE_DIR.parent
))
thread_control_work_dir.start()

build_tk_interface()
tk_interface.start()
# thread.join()
