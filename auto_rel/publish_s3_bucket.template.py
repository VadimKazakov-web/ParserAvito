# Создание клиента
from pathlib import Path
import boto3
from botocore.client import Config
from auto_rel import VERSION_PROG_FILE

BUCKET = {'Name': '---'} # <--- заменить
FILENAME_PROG = Path("../dist/ParserAvito.exe")
s3 = boto3.client(
        's3',
        endpoint_url='https://s3.twcstorage.ru',
        region_name='ru-1',
        aws_access_key_id='---', # <--- заменить
        aws_secret_access_key='---', # <--- заменить
        config=Config(s3={'addressing_style': 'path'})
    )

s3.upload_file(Filename=FILENAME_PROG, Bucket=BUCKET['Name'], Key=FILENAME_PROG.name)
s3.upload_file(Filename=VERSION_PROG_FILE, Bucket=BUCKET['Name'], Key=VERSION_PROG_FILE.name)
