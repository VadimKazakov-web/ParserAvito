# -*- coding: utf-8 -*-
import sys
import subprocess


def run_command(command_list):
    complete_process = subprocess.run(command_list, capture_output=True, shell=True)
    if complete_process.returncode == 0:
        print(complete_process.stdout.decode(encoding='oem'))
        print(f'{command_list} done')
    else:
        print(complete_process.stdout.decode(encoding='oem'))
        print(complete_process.stderr.decode(encoding='oem'))
        print(f'{command_list} error')


new_tag = sys.argv[1]
commit_message = sys.argv[2]

git_add = ["git", "add", "."]
run_command(git_add)
git_commit = ["git", "commit", "-m", commit_message]
run_command(git_commit)
