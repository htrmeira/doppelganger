#!/bin/bash
SOURCE=`cat source.list`

umount /media/heitor/windows
mkdir -p /media/heitor/windows && mount /dev/sda7 /media/heitor/windows && /bin/bash exec-backup.sh -p -i -d /media/heitor/amon/backup/ -s $SOURCE
#/bin/bash exec-backup.sh -p -i -d /media/heitor/amon/backup/ -s $SOURCE
