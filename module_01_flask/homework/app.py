import datetime
from datetime import timedelta
from flask import Flask
import random
import os
import re

app = Flask(__name__)


@app.route('/hello_world')
def print_greeting() -> str:
    return 'Привет, мир!'


@app.route('/cars')
def print_cars_list() -> str:
    return 'Chevrolet, Renault, Ford, Lada'


@app.route('/cats')
def print_cat_breed() -> str:
    cats = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
    return random.choice(cats)

@app.route('/get_time/now')
def print_current_time() -> str:
    current_time = datetime.datetime.now()
    return f'Точное время: {current_time}'


@app.route('/get_time/future')
def print_hour_past_current_time() -> str:
    current_time_after_hour = datetime.datetime.now() + timedelta(hours=1)
    return f'Точное время через час будет {current_time_after_hour}'


@app.route('/get_random_word')
def print_word() -> str:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

    with open(BOOK_FILE) as book:
        text = book.read()
        result = re.split(r'[\s]', text)
        word = random.choice(result)
    return word

visits = 0
@app.route('/counter')
def print_visits_count():
    global visits
    visits += 1
    return f'Страницу посещали {visits} раз'




if __name__ == '__main__':
    app.run(debug=True)
