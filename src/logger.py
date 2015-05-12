import logging.config

class Logger:
    _instance = None
    logger = None
    _conf_file = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, conf):
        Logger._conf_file = conf

    @staticmethod
    def getLogger(name=None):
        if not Logger.logger:
            logging.config.fileConfig(Logger._conf_file)
            Logger.logger = logging.getLogger(str(name))
            return Logger.logger
        else:
            return Logger.logger
