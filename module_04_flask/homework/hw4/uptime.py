"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask
import subprocess

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    result = subprocess.run(['uptime'], capture_output=True, text=True)
    uptime_info = result.stdout.split(',')[0]
    return f"Current uptime is {uptime_info}"


if __name__ == '__main__':
    app.run(debug=True)
