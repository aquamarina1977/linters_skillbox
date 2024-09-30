import requests
import sqlite3
import time
import threading

# URL для получения данных
url = 'https://www.swapi.tech/api/people/'


# Функция для создания таблицы в БД
def create_db():
    conn = sqlite3.connect('star_wars.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name TEXT,
            birth_year TEXT,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Функция для сохранения данных в БД
def save_to_db(name, birth_year, gender):
    conn = sqlite3.connect('star_wars.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO characters (name, birth_year, gender)
        VALUES (?, ?, ?)
    ''', (name, birth_year, gender))
    conn.commit()
    conn.close()


# Функция для получения данных о персонаже
def get_character_data(id):
    response = requests.get(url + str(id))
    if response.status_code == 200:
        data = response.json()['result']['properties']
        return data['name'], data['birth_year'], data['gender']
    else:
        return None, None, None


# Последовательные запросы
def sequential_requests():
    start_time = time.time()

    create_db()
    for i in range(1, 21):
        name, birth_year, gender = get_character_data(i)
        if name:
            save_to_db(name, birth_year, gender)

    print(f"Время выполнения последовательных запросов: {time.time() - start_time} секунд")


# Параллельные запросы с потоками
def parallel_requests():
    start_time = time.time()

    create_db()
    threads = []

    def fetch_and_save(id):
        name, birth_year, gender = get_character_data(id)
        if name:
            save_to_db(name, birth_year, gender)

    for i in range(1, 21):
        thread = threading.Thread(target=fetch_and_save, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Время выполнения параллельных запросов: {time.time() - start_time} секунд")


sequential_requests()
parallel_requests()
