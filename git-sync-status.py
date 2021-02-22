#!/usr/bin/python3

import sys, os
import configparser
import socket
import subprocess
import datetime
from pathlib import Path

def ensure_path_exists(*folders):
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

RC = Path.home() / '.git-sync-status'

cfg = configparser.ConfigParser()
cfg.read(RC)
global_cfg = cfg['global']
projects_folder = Path(global_cfg['projects_folder']).expanduser()
sync_folder = Path(global_cfg['sync_folder']).expanduser()
hostname = socket.gethostname()
hostname_sync_folder = sync_folder / hostname

# make folders
ensure_path_exists(projects_folder, hostname_sync_folder)

# for each project, do git status and copy that information
for folder in projects_folder.iterdir():
    foldername = folder.name
    
    if folder.is_dir():
        try:
            out = subprocess.check_output(
                'git status --porcelain',
                cwd=folder,
                shell=True,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            continue # non-zero exit status (not repository
        
        out = ''.join(str(out, 'utf-8'))
        
        sync_file = hostname_sync_folder / (foldername+'.txt')
        write = True
        try:
            with sync_file.open() as f:
                if out == f.read():
                    write = False # file contents match, don't write
        except FileNotFoundError:
            pass # write
        
        if write:
            print('Syncing', foldername + '...')
            with sync_file.open('w') as f:
                f.write(out)

with (hostname_sync_folder / 'timestamp').open('w') as f:
    ts = datetime.datetime.now()
    f.write(str(ts))
    print('Done @', ts)

