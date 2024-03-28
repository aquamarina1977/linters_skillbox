import sys

dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'fileFormatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%Z'
        },
        'consoleFormatter': {
            'format': '%(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%Z'
        }
    },
    'handlers': {
        'consoleHandler': {
            'class': 'StreamHandler',
            'level': 'WARNING',
            'formatter': 'consoleFormatter',
            'args': (sys.stdout,)
        },
        'fileHandler': {
            'class': 'FileHandler',
            'level': 'DEBUG',
            'formatter': 'fileFormatter',
            'args': ('logfile.log',)
        }
    },
    'loggers': {
        'root': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler']
        },
        'appLogger': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler', 'fileHandler'],
            'qualname': 'appLogger',
            'propagate': 0
        }
    }
}