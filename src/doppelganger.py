#!/usr/bin/python

import parsers

from logger import Logger

args_parser = parsers.DoppelgangerArgsParser()
config_parser = parsers.DoppelgangerConfigParser(args_parser)

# (@htrmeira): Creates a loggin instance before importing rsync
logging = Logger(config_parser.get_log_conf_file())

from argparse import ArgumentParser as arg_parser
from datetime import datetime
from rsync import DoppelgangerRsync

import os
import re

log = logging.getLogger(__name__)

class Doppelganger:

    def get_dst_dir(self):
        """
        Creates the directory name based on a the format: backup-YEAR-MONTH-DAY_HOUR-MINUTE-SECOND,
        the datetime information will come from the current time.
        """
        current = datetime.now()
        return config_parser.get_dst() + os.path.sep + ("backup-%04d-%02d-%02d_%02d-%02d-%02d" % (current.year, current.month, current.day, current.hour, current.minute, current.second))

    def get_last_dir(self):
        """
        Gets the last directory created to backup.
        It will search for directories inside the base dir that follows the specified format to dir names.
        If no directory is found, None is returned.

        Remember that directories will be sorted by name, not by ctime.
        """
        dirs = os.listdir(config_parser.get_dst())
        dirs.sort()

        # (@htrmeira): If there is no directory, return None
        backup_dirs = [None]

        for backup_dir in dirs:
            if os.path.isdir(os.path.join(config_parser.get_dst(), backup_dir)):
                true_backup_dir = re.search("backup-[0-9]+-[0-9]+-[0-9]+_[0-9]+-[0-9]+-[0-9]+", backup_dir)
                if true_backup_dir:
                    backup_dirs.append(true_backup_dir.group(0))
        return backup_dirs[-1]

    def execute(self):
        """
        Executes rsync command with the provided configuration.
        """
        last_dir = self.get_last_dir()
        if last_dir:
            last_dir = config_parser.get_dst() + os.path.sep + last_dir

        # (@htrmeira):  TODO: diff and full should depend on the amount of backups and how old are they
        # For now we will always force a diff backup.
        rsync = DoppelgangerRsync(copy_type="diff", src_dirs=config_parser.get_src(), dst_dir=self.get_dst_dir(),
                exclude_dirs=config_parser.get_exclude_dirs(), last_backup_dir=last_dir)
        rsync.execute()

if __name__ == "__main__":
    doppelganger = Doppelganger()
    doppelganger.execute()
