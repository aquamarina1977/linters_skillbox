"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

from flask import Flask
from datetime import datetime

app = Flask(__name__)

weekdays = ["понедельника", "вторника", "среды", "четверга", "пятницы", "субботы", "воскресенья"]

@app.route('/hello-world/')
def hello_world():
    today_weekday = weekdays[datetime.today().weekday()]
    return f"Привет, Петя. Хорошего {today_weekday}!" if datetime.today().weekday() in (0, 1, 3, 6) \
        else f"Привет, Петя. Хорошей {today_weekday}!"


if __name__ == '__main__':
    app.run(debug=True)