import logging

def get_logger(name):
    print("==> LEVEL: %s" % (logging.DEBUG))
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s->%(funcName)s():%(lineno)s - %(message)s')

    file_handler = logging.FileHandler('/tmp/hello.log')
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    return logger
