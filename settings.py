# -*- coding: utf-8 -*-
from pathlib import Path
from utills.utils import get_desktop_path, get_pyinstaller_work_dir, get_drive_path

VERSION = "1.0.0"

APP_NAME = "ParserAvito"

SCHTASKS_NAME = "parser_avito"

DRIVE_PATH = get_drive_path()
BASE_DIR = Path(get_desktop_path()) / Path("ParserAvitoOutput")
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

DB_TABLE_NAME = "announcement"

TIMEOUT_EXCEPTIONS_COUNTER = 4

TIMEOUT = 6

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

PYINSTALLER_WORK_DIR_RM = False
PYINSTALLER_WORK_DIR = get_pyinstaller_work_dir("pyinstaller_work_folder")

# parsing
LEFT_BLOCK_ANNOUNCEMENT_CSS = ".d9134745e0e171a2"
RIGHT_BLOCK_ANNOUNCEMENT_CSS = "._58fc8f170622acf7"

# download program
URL_S3_BUCKET_PROG = "https://s3.twcstorage.ru/parser-avito-download/ParserAvito/ParserAvito.exe"
URL_S3_BUCKET_XML = "https://s3.twcstorage.ru/parser-avito-download/ParserAvito/parser.xml"



