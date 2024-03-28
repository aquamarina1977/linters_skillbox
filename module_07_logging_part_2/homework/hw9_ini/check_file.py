import logging.config
from dict_config import dict_config
import logging

logging.config.dictConfig(dict_config)

app_logger = logging.getLogger("appLogger")

app_logger.debug("logger debug level")
app_logger.info('logger info level')
app_logger.warning('logging warning level')


