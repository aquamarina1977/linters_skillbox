import logging.config
from dict_config import dict_config

logging.config.fileConfig('logging_conf.ini')
logging.config.dictConfig(dict_config)
