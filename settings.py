# -*- coding: utf-8 -*-
import os
from pathlib import Path

BASE_DIR = Path(os.getcwd()) / Path("ParserAvitoOutput")
if not BASE_DIR.exists():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
os.environ["BASE_DIR"] = str(BASE_DIR)

LOG_DIR = BASE_DIR / Path("log")
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
os.environ["LOG_DIR"] = str(LOG_DIR)

LOG_FILE = Path("logbook.log")
os.environ["LOG_FILE"] = str(LOG_FILE)

DATABASE_DIR = BASE_DIR / Path('database')
if not DATABASE_DIR.exists():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
os.environ["DATABASE_DIR"] = str(DATABASE_DIR)

DATABASE = DATABASE_DIR / Path('data.db')
os.environ["DATABASE"] = str(DATABASE)

TIMEOUT_EXCEPTIONS_COUNTER = 4
os.environ["TIMEOUT_EXCEPTIONS_COUNTER"] = str(TIMEOUT_EXCEPTIONS_COUNTER)

TIMEOUT = 5
os.environ["TIMEOUT"] = str(TIMEOUT)

TOP_ANNOUNCEMENT = 100
