# -*- coding: utf-8 -*-
from pathlib import Path
import sys
sys.path.append("")
import os
from auto_rel.settings import VERSION_PROG_FILE
import boto3
from botocore.client import Config
from dotenv import load_dotenv
load_dotenv()

"""
Скрипт загружает в bucket скомпилированную программу и файл с номером версии
"""

BUCKET = {'Name': os.getenv("BUCKET_NAME")}
FILENAME_PROG = Path(os.getcwd()) / Path("dist") / Path("ParserAvito.exe")
s3 = boto3.client(
        's3',
        endpoint_url=os.getenv("ENDPOINT_URL"),
        region_name=os.getenv("REGION_NAME"),
        aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
        config=Config(s3={'addressing_style': 'path'})
    )

s3.upload_file(Filename=FILENAME_PROG, Bucket=BUCKET['Name'], Key=FILENAME_PROG.name)
s3.upload_file(Filename=VERSION_PROG_FILE, Bucket=BUCKET['Name'], Key=VERSION_PROG_FILE.name)

