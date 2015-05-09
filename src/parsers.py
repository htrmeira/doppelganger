from argparse import ArgumentParser as arg_parser

import ConfigParser as config_parser
import sys

class DoppelgangerConfigParser:
    DEFAULT_SECTION = "default"

    def __init__(self, parser=None):
        self.parser = parser.get_parser()
        self.config = config_parser.SafeConfigParser({"verbose" : "False" })
        self.config.read(self.parser.conf)

    def get_src(self):
        if self.parser.src is not None:
            return self.parser.src
        else:
            return self.config.get(self.DEFAULT_SECTION, "src_dirs").split(',')

    def get_dst(self):
        if self.parser.dst is not None:
            return self.parser.dst
        else:
            return self.config.get(self.DEFAULT_SECTION, "dst_dir")

    def is_verbose(self):
        if self.parser.verbose is not None:
            return self.parser.verbose
        else:
            return self.config.get(self.DEFAULT_SECTION, "verbose")

class DoppelgangerArgsParser:

    def get_parser(self):
        parser = arg_parser(prog="doppelganger", description="Backup tool")
        parser.add_argument('-s', "--src", type=str, metavar="SRC_DIR", nargs='+', help="list of source dirs to backup")
        parser.add_argument('-d', "--dst", type=str, metavar="DST_DIR", nargs=1, help="destination directory")
        parser.add_argument('-c', "--conf", required=True, type=str, metavar="CONF_FILE", nargs=1, help="configuration file")
        parser.add_argument('-v', "--verbose", action='store_true', help="configuration file")
        return parser.parse_args()
