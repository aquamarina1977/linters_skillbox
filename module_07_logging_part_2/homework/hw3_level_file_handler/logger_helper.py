import logging
import sys


class LevelFileHandler(logging.Handler):
    def __init__(self, level, filename):
        super().__init__(level)
        self.filename = filename

    def emit(self, record):
        with open(self.filename, "a") as file:
            file.write(self.format(record))
            file.write("\n")


def get_logger(name):
    formatter = logging.Formatter(fmt="%(asctime)s | %(name)s | %(levelname)s | %(lineno)d | %(message)s")
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    debug_handler = LevelFileHandler(logging.DEBUG, "calc_debug.log")
    error_handler = LevelFileHandler(logging.ERROR, "calc_error.log")

    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)

    debug_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    return logger

