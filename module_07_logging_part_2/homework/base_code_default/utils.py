
from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging

logger = logging.getLogger("string_to_operator")
logger.setLevel(logging.ERROR)

# Создаем обработчик для вывода ошибок в файл
error_handler = logging.FileHandler("error.log")
error_handler.setLevel(logging.ERROR)

# Создаем форматтер для обработчика
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
error_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(error_handler)

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        logging.error(f"wrong operator type {value}")
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logging.error(f"wrong operator value {value}")
        raise ValueError("wrong operator value")

    return OPERATORS[value]

