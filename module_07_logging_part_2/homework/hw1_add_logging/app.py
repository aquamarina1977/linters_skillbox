
import sys
from utils import string_to_operator
import logging

logger = logging.getLogger('app')
logger.setLevel('DEBUG')
def calc(args):
    logging.debug(f"Arguments: {args=}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logging.exception(f"Error while converting number 1\n{e}")

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logging.exception(f"Error while converting number 1\n{e}")

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logging.info(f"Result: {result}")
    logging.debug(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    #calc(sys.argv[1:])
    calc('2+3')