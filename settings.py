# -*- coding: utf-8 -*-
from pathlib import Path
from version import version
from backend.utils.utils import get_desktop_path, app_work_dir

APP_NAME = "ParserAvito"

VERSION = version

SCHTASKS_NAME = "parser_avito"

APP_TEMPORARY = app_work_dir("parser_avito_temp")
APP_TEMPORARY.mkdir(exist_ok=True)

BASE_DIR = Path(get_desktop_path()) / Path("ParserAvitoOutput")
BASE_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = BASE_DIR / Path("log")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = Path("logbook.log")

COOKIE_FILE = BASE_DIR / Path("cookie") / Path("cookie.txt")

DATABASE_DIR = APP_TEMPORARY / Path('database')
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE = DATABASE_DIR / Path('data.db')

DB_TABLE_NAME = "announcement"

TIMEOUT_EXCEPTIONS_COUNTER = 8

TIMEOUT = 9

TOP_ANNOUNCEMENT = 100

# tkinter interface
FONT_SIZE = 13
BACKGROUND_COLOR = "#2F4F4F"
FOREGROUND_COLOR = "white"
BACKGROUND_COLOR_ENTRY = "white"
FOREGROUND_COLOR_ENTRY = "#000000"
BACKGROUND_COLOR_BTN = "white"
FOREGROUND_COLOR_BTN = "#000000"
COLOR_FOR_HOVER = "#778899"
WIDTH_LABEL = 50

# parsing
LEFT_BLOCK_ANNOUNCEMENT_CSS = ".d9134745e0e171a2"
RIGHT_BLOCK_ANNOUNCEMENT_CSS = "._58fc8f170622acf7"

# download program
URL_S3_BUCKET_PROG = "https://s3.twcstorage.ru/parser-avito-download/ParserAvito.exe"
URL_S3_BUCKET_XML = "https://s3.twcstorage.ru/parser-avito-download/parser.xml"
URL_S3_BUCKET_VERSION_PROG = "https://s3.twcstorage.ru/parser-avito-download/version.py"

DRIVER_IMPLICITLY_WAIT = 30



