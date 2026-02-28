# -*- coding: utf-8 -*-
import os
from pathlib import Path

VERSION = "Beta"
APP_NAME = Path("ParserAvito")

BASE_DIR = Path(os.getcwd()) / Path("ParserAvitoOutput")
if not BASE_DIR.exists():
    BASE_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = BASE_DIR / Path("log")
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = Path("logbook.log")

DATABASE_DIR = BASE_DIR / Path('database')
if not DATABASE_DIR.exists():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE = DATABASE_DIR / Path('data.db')

TIMEOUT_EXCEPTIONS_COUNTER = 4

TIMEOUT = 5

TOP_ANNOUNCEMENT = 100

# tkinter interface
FONT_SIZE = 13
BACKGROUND_COLOR = "#0000CD"
FOREGROUND_COLOR = "white"
BACKGROUND_COLOR_ENTRY = "white"
FOREGROUND_COLOR_ENTRY = "#000000"
BACKGROUND_COLOR_BTN = "white"
FOREGROUND_COLOR_BTN = "#000000"
COLOR_FOR_HOVER = "#00BFFF"
WIDTH_LABEL = 50

REPOSITORY = "https://github.com/VadimKazakov-web/ParserAvito.git"
REPOSITORY_TAGS = "https://github.com/VadimKazakov-web/ParserAvito/tags"
