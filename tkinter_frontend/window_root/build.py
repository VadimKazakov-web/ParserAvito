# -*- coding: utf-8 -*-
from tkinter_frontend.root.root import WindowRoot
import logging

window = WindowRoot("ParserAvitoSelenium")
ROOT = window.get_root()
logging.info("{}: done".format(__name__))

