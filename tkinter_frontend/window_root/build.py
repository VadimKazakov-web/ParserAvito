# -*- coding: utf-8 -*-
from tkinter_frontend import WindowRoot
import logging
from settings import APP_NAME, VERSION

window = WindowRoot(f"{APP_NAME}({VERSION})")
logging.info("{}: done".format(__name__))

