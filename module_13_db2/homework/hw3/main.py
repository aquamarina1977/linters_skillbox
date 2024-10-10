import datetime
import sqlite3

def create_table_if_not_exists(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS birds_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bird_name TEXT NOT NULL,
            date_time TEXT NOT NULL
        )
    """)

def log_bird(cursor: sqlite3.Cursor, bird_name: str, date_time: str) -> None:
    # Добавляем запись о новой птице в БД
    cursor.execute("""
        INSERT INTO birds_log (bird_name, date_time)
        VALUES (?, ?)
    """, (bird_name, date_time))
def check_if_such_bird_already_seen(cursor: sqlite3.Cursor, bird_name: str) -> bool:
    # Проверяем, существует ли запись с такой птицей в БД
    cursor.execute("""
        SELECT EXISTS(
            SELECT 1
            FROM birds_log
            WHERE bird_name = ?
        )
    """, (bird_name,))
    return cursor.fetchone()[0] == 1


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("birds.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        create_table_if_not_exists(cursor)
        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
        else:
            log_bird(cursor, name, right_now)
            print("Это новая запись!")

