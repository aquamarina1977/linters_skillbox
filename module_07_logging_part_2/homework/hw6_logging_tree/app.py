
import sys
from utils import string_to_operator
from logger_helper import get_logger
import logging_tree

logger = get_logger('app')

def calc(args):
    logger.debug(f"Arguments: {args=}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.exception(f"Error while converting number 1\n{e}")

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.exception(f"Error while converting number 1\n{e}")

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.info(f"Result: {result}")
    logger.debug(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    #calc(sys.argv[1:])
    calc('2+3')
    #logging_tree.printout()
    with open('logging_tree.txt', 'w') as f:
        print(logging_tree.format.build_description(), file=f)

