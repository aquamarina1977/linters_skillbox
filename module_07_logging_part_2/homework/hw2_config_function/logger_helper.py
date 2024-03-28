import logging
import sys

def get_logger(name):
    formatter = logging.Formatter(fmt="%(asctime)s | %(name)s | %(levelname)s | %(lineno)d | %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level='DEBUG')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger