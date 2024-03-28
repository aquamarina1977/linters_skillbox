import logging

class ASCIIFilter(logging.Filter):
    def filter(self, record):
        if all(ord(c) < 128 for c in record.msg) is True:
            return True
        return False


dict_config = {
    "version": 1.0,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(filename)s | %(asctime)s | %(lineno)d | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filters": ["ascii_filter"]
        }
    },
    "loggers": {
        "module_logger": {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    },
    "filters": {
        "ascii_filter": {
            "()": ASCIIFilter
        }
    }
}

