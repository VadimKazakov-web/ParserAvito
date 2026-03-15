# Создание клиента
import uuid
from pathlib import Path

import boto3
from botocore.client import Config

BUCKET = {'Name': '---'} # <--- заменить
FILENAME = Path("dist/ParserAvito.exe")
s3 = boto3.client(
        's3',
        endpoint_url='https://s3.twcstorage.ru',
        region_name='ru-1',
        aws_access_key_id='---', # <--- заменить
        aws_secret_access_key='---', # <--- заменить
        config=Config(s3={'addressing_style': 'path'})
    )

s3.upload_file(Filename=FILENAME, Bucket=BUCKET['Name'], Key='ParserAvito_test.exe')
