import os
from colorama import init as colorama_init, Fore
import subprocess

colorama_init()

repo_path = 'C:/workspace/cps/'

GIT_CMD_FMT = 'git -C {} {}'

IGNORE_DIRS = [
    '.idea',
    'cps'
]

REPOS = os.listdir(repo_path)
NUM_REPOS = len(REPOS)

Repo_Count = 0


for d in REPOS:
    Repo_Count += 1
    
    if d in IGNORE_DIRS:
        info(f'Ignoring {d}...')
        continue

    abs_path = repo_path + d + '/'

    if not is_git_dir(abs_path):
        warn(f'{d} is not a Git directory! Skipping...')
        continue

    status_cmd = GIT_CMD_FMT.format(abs_path, 'status')

    status_output = str(subprocess.check_output(status_cmd, shell=True), 'utf-8')

    # Skip REPOS not on master
    if not 'on branch master' in status_output.lower():
        branch = status_output.split('\n')[0].split(' ')[2]
        info(f'{d} is on branch {branch}.. Skipping!')
        print()
        continue

    # Don't pull master with unstaged changes
    if 'modified' in status_output:
        error(f'{d} has unstaged changes on master!')
        print(status_output)
        continue
    
    info(f'Pulling {d}/origin/master...')

    pull_cmd = GIT_CMD_FMT.format(abs_path, 'pull')

    subprocess.call(pull_cmd, shell=True)
    print()

input('Press any key to close...')
