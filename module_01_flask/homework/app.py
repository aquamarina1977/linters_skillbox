import datetime
from datetime import timedelta
from flask import Flask
import random
import os
import re

app = Flask(__name__)


@app.route('/hello_world')
def test_function():
    print('Привет, мир!')


@app.route('/cars')
def test_function():
    print('Chevrolet, Renault, Ford, Lada')


@app.route('/cats')
def test_function():
    cats = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
    print(random.choice(cats))

@app.route('/get_time/now')
def test_function():
    current_time = datetime.datetime.now()
    print(f'Точное время: {current_time}')


@app.route('/get_time/future')
def test_function():
    current_time_after_hour = datetime.datetime.now() + timedelta(hours=1)
    print(f'Точное время через час будет {current_time_after_hour}')


@app.route('/get_random_word')
def test_function():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

    with open(BOOK_FILE) as book:
        text = book.read()
        result = re.split(r'[\s]', text)
        print(random.choice(result))

visits = 0
@app.route('/counter')
def test_function():
    global visits
    visits += 1
    print(f'Страницу посещали {visits} раз')




if __name__ == '__main__':
    app.run(debug=True)
