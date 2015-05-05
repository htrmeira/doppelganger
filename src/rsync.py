import subprocess
from subprocess import PIPE

import logging.config

# It seems to be static, so we jsut need to declare on main class
logging.config.fileConfig('../etc/logging.conf')
log = logging.getLogger(__name__)

class DoppelgangerRsync:

    def __init__(self, copy_type="full", src_dirs=None, dst_dir=None, exclude_dirs=None, last_backup_dir=None):
        """
        Executes rsync over the specified files and directories copying to the specified directory.

        @copy_type [full, diff]: string specifying if the is a full copy or incremental one. MANDATORY
        @src_dirs: list of directories to copy. MANDATORY
        @dst_dir: destination directory of the copies. MANDATORY
        @exclude_dirs: directories or files that are inside @src_dirs but must not be copied.
        @last_backup_dir: last copy directory to compare in case of incremental (diff) copy.
                        This is mandatory for incremental copy, since a reference directory is necessary.

        """
        self.copy_type = copy_type
        self.last_backup_dir = last_backup_dir
        self.src_dirs = src_dirs
        self.exclude_dirs = exclude_dirs
        self.dst_dir = dst_dir
        log.debug("Intializing...")

    def execute(self):
        """
        Properly executes the copy based on the type.
        This is a blocking method.
        """
        if self.copy_type is "full":
            log.debug("Executing full backup: copy_type=%s, src_dirs=%s, dst_dir=%s, exclude_dirs=%s, last_backup_dir=%s"
                    % (self.copy_type, self.src_dirs, self.dst_dir, self.exclude_dirs, self.last_backup_dir))
            self.execute_full()
        elif self.copy_type is "diff":
            log.debug("Executing diff backup: copy_type=%s, src_dirs=%s, dst_dir=%s, exclude_dirs=%s, last_backup_dir=%s"
                    % (self.copy_type, self.src_dirs, self.dst_dir, self.exclude_dirs, self.last_backup_dir))
            self.execute_diff()
        else:
            log.error("You must specify the type of backup as 'full' or 'diff'")
            raise RsyncValidationError("copy type must be full or diff, but it was %s" % (self.copy_type))

    def raw_rsync_command(self):
        """
        Creates a list with a simple rsync command common to the supported copy types.

        The specified arguments here are:
        --delete: delete extraneous files from dest dirs
        --recursive: tells rsync to copy directories recursively.
        --hard-links: preserve hard links
        --perms: preserve permissions
        --owner: preserve owner
        --group: preserve group
        --times: preserve modification times
        --devices: preserve device files
        --specials: preserve special files
        --links: copy symlinks as symlinks
        """
#        command = ["rsync", "--delete", "--recursive", "--hard-links", "--archive", "--progress"]
        command = ["rsync", "--delete", "--recursive", "--hard-links", "--progress",
                "--perms", "--owner", "--group", "--times", "--devices", "--specials",
                "--links"]

        if self.exclude_dirs is not None:
            for exclude_dir in self.exclude_dirs:
                command.append("--exclude=%s" % (exclude_dir))
        return command

    def execute_full(self):
        """
        Executes a full copy of the directories.

        The mandatories parameters src_dirs and dst_dir must be declared at this point
        """
        command = self.raw_rsync_command()
        for src_dir in self.src_dirs:
            command.append(src_dir)
        command.append(self.dst_dir)
        self.executes_command(command)

    def execute_diff(self):
        """
        Executes a copy copy of the directories.

        The parameters src_dirs, dst_dir and last_backup_dir must be declared at this point

        The specified arguments here are:
        --link-dest: hardlink to files in DIR when unchanged
        """
        command = self.raw_rsync_command()

        if self.last_backup_dir is not None:
            command.append("--link-dest=%s" % (self.last_backup_dir))

        for src_dir in self.src_dirs:
            command.append(src_dir)

        command.append(self.dst_dir)
        self.executes_command(command)

    def executes_command(self, command):
        """
        Creates a new process to execute the given comand.
        The command must be in a list, where each argument is an element.
        This is a blocking method, since we are using the stdout and stderr of the process.
        """
        log.info("Executing command: %s" % (command))
        proc = subprocess.Popen(command, shell=False, stdout=PIPE, stderr=PIPE)
        self.stream_watcher("stdout", proc.stdout)
        self.stream_watcher("stderr", proc.stderr)

    def stream_watcher(self, identifier, stream):
        """
        Consumes the lines outputed by stdout and stderr, wating when necessary.
        By the end of the execution, it will close the stream.
        """
        for line in stream:
            self.send(line)
            stream.flush()

        if not stream.closed:
            stream.close()

    def send(self, line):
        """
        Send the line to the added listeners.
        """
        # TODO Should do more than log the output.
        # In the future we are planning to create a progress bar based on this output.
        log.debug("rsync -> %s" % (line))

class RsyncValidationError(Exception):

    def __init__(self, message):
        super(RsyncValidationError, self).__init__(message)

if __name__ == "__main__":
    #src_dirs = ["/tmp/doppelganger/test1", "/tmp/doppelganger/test2", "/tmp/doppelganger/test3", "/home/heitor/Downloads"]
    src_dirs = ["/home/heitor/Documents", "/home/heitor/Downloads"]
    dst_dir = "/media/heitor/amon/teste-2"
    last_backup_dir = "/media/heitor/amon/teste"
#    exclude_dirs = ["/home/heitor/Downloads/teste", "/home/heitor/Downloads/teste2"]
    exclude_dirs = ["Downloads/teste", "Downloads/teste2"]

    rsync = DoppelgangerRsync(copy_type="diff", src_dirs=src_dirs, dst_dir=dst_dir, exclude_dirs=exclude_dirs, last_backup_dir=last_backup_dir)
    rsync.execute()
