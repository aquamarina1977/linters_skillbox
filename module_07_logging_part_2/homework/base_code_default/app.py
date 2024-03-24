
import sys
from utils import string_to_operator
import logging
import decorator

@decorator.loger
def calc(args):
    logging.info("Arguments: ", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logging.debug("Error while converting number 1")
        logging.debug(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logging.debug("Error while converting number 1")
        logging.debug(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    print(f"{num_1} {operator} {num_2} = {result}")
    return f"Result: {result}"


if __name__ == '__main__':
    # calc(sys.argv[1:])
    calc('2+3')
