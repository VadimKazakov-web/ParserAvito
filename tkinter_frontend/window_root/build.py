# -*- coding: utf-8 -*-
from tkinter_frontend.root.root import WindowRoot
import logging
from settings import APP_NAME, VERSION

window = WindowRoot(f"{APP_NAME}[{VERSION}]")
ROOT = window.get_root()
logging.info("{}: done".format(__name__))

