import operator
from flask import Flask, jsonify, request
from flask_jsonrpc import JSONRPC
from jsonrpc.exceptions import JSONRPCInvalidRequestException, JSONRPCException

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    Сложение двух чисел.

    Пример запроса:
    {
        "jsonrpc": "2.0",
        "method": "calc.add",
        "params": {"a": 7.8, "b": 5.3},
        "id": "1"
    }

    Пример ответа:
    {
        "id": "1",
        "jsonrpc": "2.0",
        "result": 13.1
    }
    """
    return operator.add(a, b)

@jsonrpc.method('calc.subtract')
def subtract(a: float, b: float) -> float:
    """
    Вычитание двух чисел.

    Пример запроса:
    {
        "jsonrpc": "2.0",
        "method": "calc.subtract",
        "params": {"a": 10.5, "b": 4.2},
        "id": "2"
    }

    Пример ответа:
    {
        "id": "2",
        "jsonrpc": "2.0",
        "result": 6.3
    }
    """
    return operator.sub(a, b)

@jsonrpc.method('calc.multiply')
def multiply(a: float, b: float) -> float:
    """
    Умножение двух чисел.

    Пример запроса:
    {
        "jsonrpc": "2.0",
        "method": "calc.multiply",
        "params": {"a": 3.0, "b": 4.0},
        "id": "3"
    }

    Пример ответа:
    {
        "id": "3",
        "jsonrpc": "2.0",
        "result": 12.0
    }
    """
    return operator.mul(a, b)

@jsonrpc.method('calc.divide')
def divide(a: float, b: float) -> float:
    """
    Деление двух чисел.

    Пример запроса:
    {
        "jsonrpc": "2.0",
        "method": "calc.divide",
        "params": {"a": 10.0, "b": 2.0},
        "id": "4"
    }

    Пример ответа:
    {
        "id": "4",
        "jsonrpc": "2.0",
        "result": 5.0
    }

    Ошибка:
    {
        "jsonrpc": "2.0",
        "error": {
            "code": -32602,
            "message": "Division by zero is not allowed."
        },
        "id": "5"
    }
    """
    if b == 0:
        raise JSONRPCException('Division by zero is not allowed.')
    return operator.truediv(a, b)

@app.errorhandler(JSONRPCInvalidRequestException)
def handle_invalid_request(error):
    return {
        'jsonrpc': '2.0',
        'error': {'code': -32600, 'message': str(error)},
        'id': None
    }, 400

@app.errorhandler(JSONRPCException)
def handle_invalid_params(error):
    return {
        'jsonrpc': '2.0',
        'error': {'code': -32602, 'message': str(error)},
        'id': None
    }, 400

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
