# -*- coding: utf-8 -*-
import sys
import subprocess
from pathlib import Path

"""Модуль для автоматизации рутинных команд для релиза, добавлен в репозиторий чтобы не забыть"""


def run_command(command_list):
    complete_process = subprocess.run(command_list, capture_output=True, shell=True)
    if complete_process.returncode == 0:
        print(complete_process.stdout.decode(encoding='oem'))
        print(complete_process.stdout.decode(encoding='utf-8'))
        print(f'{command_list} done')
    else:
        print(complete_process.stdout.decode(encoding='oem'))
        print(complete_process.stderr.decode(encoding='oem'))
        print(f'{command_list} error')


VERSION_PROG_FILE = Path("version.txt")

print(sys.argv)
new_tag = sys.argv[1]
commit_message = sys.argv[2]

VERSION_PROG_FILE.write_text(new_tag)

git_add = ["git", "add", "."]
run_command(git_add)

git_commit = ["git", "commit", "-m", commit_message]
run_command(git_commit)

git_add_new_tag = ["git", "tag", "-a", new_tag, "-m", new_tag]
run_command(git_add_new_tag)

pyinstaller_compile = ["pyinstaller", "parser.spec"]
run_command(pyinstaller_compile)

upload_in_bucket = ["python", "publish_s3_bucket.py"]
run_command(upload_in_bucket)

git_push = ["git", "push", "origin", "main"]
run_command(git_push)

git_push_tags = ["git", "push", "origin", "--tags"]
run_command(git_push_tags)
