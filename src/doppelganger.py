from argparse import ArgumentParser as arg_parser

import parsers

class Doppelganger:
     def __init__(self, config_parser):
         print("==> init")
         print("src=%s" % (config_parser.get_src()))
         print("src=%s" % (config_parser.get_dst()))
         print("src=%s" % (config_parser.is_verbose()))

if __name__ == "__main__":
    args_parser = parsers.DoppelgangerArgsParser()
    config_parser = parsers.DoppelgangerConfigParser(args_parser)
    doppelganger = Doppelganger(config_parser)
