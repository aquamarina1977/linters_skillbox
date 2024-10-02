import multiprocessing
import requests
import sqlite3
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

url = 'https://www.swapi.tech/api/people/'

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

def save_to_db(name, birth_year, gender):
    conn = sqlite3.connect('star_wars.db')  # Corrected typo in database name
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO characters (name, birth_year, gender)
        VALUES (?, ?, ?)
    ''', (name, birth_year, gender))
    conn.commit()
    conn.close()

def get_character_data(id):
    response = requests.get(url + str(id))
    if response.status_code == 200:
        data = response.json()['result']['properties']
        return data['name'], data['birth_year'], data['gender']  # Corrected key 'birth_year'
    else:
        return None, None, None

def fetch_and_save(id):
    name, birth_year, gender = get_character_data(id)
    if name:
        save_to_db(name, birth_year, gender)

def thread_pool_requests():
    start_time = time.time()
    create_db()
    with ThreadPool(processes=50) as ex:
        ex.map(fetch_and_save, range(1, 21))

    print(f'Время выполнения с ThreadPool: {time.time() - start_time} секунд')

def process_pool_requests():
    start_time = time.time()
    create_db()
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(fetch_and_save, range(1, 21))

    print(f'Время выполнения с ProcessPool: {time.time() - start_time} секунд')

if __name__ == "__main__":
    thread_pool_requests()
    process_pool_requests()
