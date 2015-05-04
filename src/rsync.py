import subprocess
from subprocess import PIPE

import logger


log = logger.get_logger(__name__)

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
        log.info("Teste")

    def execute(self):
        """
        Properly executes the copy based on the type.
        This is a blocking method.
        """
        if self.copy_type is "full":
            self.execute_full()
        elif self.copy_type is "diff":
            print("DIFF")
        else:
            raise RsyncValidationError("copy type must be full or diff, but it was %s" % (self.copy_type))

    def raw_rsync_command(self):
        """
        Creates a list with a simple rsync command common to the supported copy types.

        The specified arguments here are:
        --delete: delete extraneous files from dest dirs
        --recursive: tells rsync to copy directories recursively.
        --hard-links: preserve hard links
        --archive: equivalent to -rlptgoD, preserve almost everything

        """
        command = ["rsync", "--delete", "--recursive", "--hard-links", "--archive", "--progress"]

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

    def executes_command(self, command):
        proc = subprocess.Popen(command, shell=False, stdout=PIPE, stderr=PIPE)
        self.stream_watcher("stdout", proc.stdout)
        self.stream_watcher("stderr", proc.stderr)

    def stream_watcher(self, identifier, stream):
        for line in stream:
#        for line in iter(stream.readline, b''):
            self.send(line)
            stream.flush()

        if not stream.closed:
            stream.close()

    def send(self, line):
        #print repr("line: %s" % (line.split()[0]))
        print("line: %s" % (line))

class RsyncValidationError(Exception):

    def __init__(self, message):
        super(RsyncValidationError, self).__init__(message)

if __name__ == "__main__":
    src_dirs = ["/tmp/doppelganger/test1", "/tmp/doppelganger/test2", "/tmp/doppelganger/test3", "/home/heitor/Downloads"]
    dst_dir = "/media/heitor/amon/teste/"
    exclude_dirs = ["/home/heitor/Downloads/teste", "/home/heitor/Downloads/teste2"]

    rsync = DoppelgangerRsync(src_dirs=src_dirs, dst_dir=dst_dir, exclude_dirs=exclude_dirs)
#    rsync.execute()
