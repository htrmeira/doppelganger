import ConfigParser as config_parser
import sys

class DoppelgangerConfigParser:
    DEFAULT_SECTION = "default"
    conf_path = None

    # @conf_path: the path of the conf file
    def __init__(self):
        self.config = config_parser.ConfigParser()
        self.config.read(conf_path)

    def get_src(self):
        return self.config.get(self.DEFAULT_SECTION, "src_dirs").split(',')

    def get_dst(self):
        return self.config.get(self.DEFAULT_SECTION, "dst_dir")

if __name__ == "__main__":
    conf_path = sys.argv[1]
    DoppelgangerConfigParser.conf_path = conf_path
    config_parser = DoppelgangerConfigParser()
    print("get_src: %s" % (config_parser.get_src()))
    print("TESTE: %s" % (DoppelgangerConfigParser.conf_path))
