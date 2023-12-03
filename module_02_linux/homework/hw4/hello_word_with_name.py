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
@app.route('/hello-world/<name>')
def hello_world(name):
    today_weekday = weekdays[datetime.today().weekday()]
    return f"Привет, {name}. Хорошего {today_weekday}!" if today_weekday in (0, 1, 3, 6) else f"Привет, {name}. Хорошей {today_weekday}!"

name = input('Введите имя: ')
print(hello_world(name))

if __name__ == '__main__':
    app.run(debug=True)