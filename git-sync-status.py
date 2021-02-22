#!/usr/bin/python3

import sys, os
import configparser
import socket
import subprocess
import datetime

def ensure_path_exists(*folders):
    for folder in folders:
        try:
            os.makedirs(folder)
        except FileExistsError:
            continue

RC = os.path.expanduser('~/.git-sync-status')

cfg = configparser.ConfigParser()
cfg.read(RC)
global_cfg = cfg['global']
projects_folder = os.path.expanduser(global_cfg['projects_folder'])
sync_folder = os.path.expanduser(global_cfg['sync_folder'])
hostname = socket.gethostname()
hostname_sync_folder = os.path.join(sync_folder, hostname)

# TODO: make folders
ensure_path_exists(projects_folder, hostname_sync_folder)

# TODO: for each project, do git status and copy that information
for folder in os.listdir(projects_folder):
    working_dir = os.path.join(projects_folder, folder)
    if os.path.isdir(working_dir):
        print('Syncing', folder + '...')
        
        try:
            out = subprocess.check_output('git status --porcelain', cwd=working_dir, shell=True)
        except subprocess.CalledProcessError:
            continue # non-zero exit status (not repository
        
        out = ''.join(str(out, 'utf-8'))
        
        sync_file = os.path.join(hostname_sync_folder, folder+'.txt')
        write = False
        try:
            with open(sync_file, 'r') as f:
                if out == f.read():
                    write = False
        except FileNotFoundError:
            write = True
        
        if write:
            with open(sync_file, 'w') as f:
                f.write(out)

with open(os.path.join(hostname_sync_folder, 'timestamp'), 'w') as f:
    ts = datetime.datetime.now()
    f.write(str(ts))
    print('Done @', ts)

