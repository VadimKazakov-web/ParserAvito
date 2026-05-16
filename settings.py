# -*- coding: utf-8 -*-
from pathlib import Path
from version import version
from backend.utils.utils import get_desktop_path, get_drive_path, app_work_dir
import random

APP_NAME = "ParserAvito"

VERSION = version

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

TIMEOUT_EXCEPTIONS_COUNTER = 8

TIMEOUT = 9

TOP_ANNOUNCEMENT = 100

# tkinter interface
FONT_SIZE = 13
BACKGROUND_COLOR = "#2eab49"
FOREGROUND_COLOR = "white"
BACKGROUND_COLOR_ENTRY = "white"
FOREGROUND_COLOR_ENTRY = "#000000"
BACKGROUND_COLOR_BTN = "white"
FOREGROUND_COLOR_BTN = "#000000"
COLOR_FOR_HOVER = "#56ccb0"
WIDTH_LABEL = 50

REPOSITORY = "https://github.com/VadimKazakov-web/ParserAvito.git"
REPOSITORY_TAGS = "https://github.com/VadimKazakov-web/ParserAvito/tags"

APP_TEMPORARY = app_work_dir("parser_avito_temp")

# parsing
LEFT_BLOCK_ANNOUNCEMENT_CSS = ".d9134745e0e171a2"
RIGHT_BLOCK_ANNOUNCEMENT_CSS = "._58fc8f170622acf7"

# download program
URL_S3_BUCKET_PROG = "https://s3.twcstorage.ru/parser-avito-download/ParserAvito.exe"
URL_S3_BUCKET_XML = "https://s3.twcstorage.ru/parser-avito-download/parser.xml"
URL_S3_BUCKET_VERSION_PROG = "https://s3.twcstorage.ru/parser-avito-download/version.py"

DEFAULT_AVITO_CATEGORY = random.choice(
    [
        "https://www.avito.ru/moskva/hobbi_i_otdyh",
        "https://www.avito.ru/moskva/mototsikly_i_mototehnika?radius=0&searchRadius=0",
        "https://www.avito.ru/moskva/avtomobili/novyy/mazda-ASgBAgICAkSGFMbmAeC2DeaYKA?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6InkiO3M6MTY6InRocnBrd3FkS2k0QWl2dzUiO31UmhE6JgAAAA&localPriority=0&radius=0&searchRadius=0",
        "https://www.avito.ru/moskva/chasy_i_ukrasheniya/chasy-ASgBAgICAUTQAYYG",
        "https://www.avito.ru/moskva/chasy_i_ukrasheniya/yuvelirnye_izdeliya-ASgBAgICAUTQAYgG",
        "https://www.avito.ru/moskva/krasota_i_zdorove/ukhod_i_gigiena-ASgBAgICAUSEAqoJ",
        "https://www.avito.ru/moskva/zapchasti_i_aksessuary?context=H4sIAAAAAAAA_wFRAK7_YToyOntzOjg6ImZyb21QYWdlIjtzOjE0OiJjYXRlZ29yeVdpZGdldCI7czo5OiJmcm9tX3BhZ2UiO3M6MTQ6ImNhdGVnb3J5V2lkZ2V0Ijt9inXVTFEAAAA&f=ASgBAgICAkQKJooL_JwB&geoCoords=55.755814%2C37.617635",
    ]
)



