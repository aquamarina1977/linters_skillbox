"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""

from flask import Flask, request
import shlex
import os

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    args = request.args.getlist('arg')
    cmd = "ps " + " ".join(shlex.quote(arg) for arg in args)
    result = os.popen(cmd).read()
    return f"<pre>{result}</pre>"


if __name__ == "__main__":
    app.run(debug=True)
