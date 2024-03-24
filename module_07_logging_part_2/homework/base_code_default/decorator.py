from typing import List
from datetime import datetime, timedelta
from functools import wraps
import logging

logger = logging.getLogger('culc_performance')
logger.setLevel(logging.INFO)

handler = logging.FileHandler('logs_for_culc.txt')
formatter = logging.Formatter(fmt="%(asctime)s, %(name)s, %(filename)s, %(lineno)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def loger(func: callable, logger=logger):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f'Arguments: {args=}')
            res = func(*args, **kwargs)
            logger.info(res)
            return res
        except Exception as e:
            error_message = f"Error: {str(e)}"
            logging.error(error_message)
    return wrapper