# git-sync-status

Syncs all your repository statuses to a sync folder (i.e. Dropbox) so you can
tell the status of each of them on every device you have.

Copyright (c) 2021 Grady O'Connell

MIT License.  See LICENSE file for details.

As with any script that modifies your files, please exercise caution when
using it with your own files, since a bug may cause data loss which I am
not responsible for.  Please report issues you find to the project's
issue tracker.  Always back up your files!  Thanks!

## Usage

- Copy git-sync-status.example to ~/.git-sync-status.
- Replace folder locations in this config file with your own.
- Run python script to sync the status information to your sync folder.
- Check the sync folder to see the data it generated.

## Information

This program uses your hostname to uniquely identify your system, so make sure
hostnames across your devices are different.  You can also check the timestamp
file to see how new the sync data is.
Running this script multiple times on the same data should only update the
timestamp file, so you shouldn't have to worry about excessive data writing
to your sync folder unless your repository status changes a lot.

