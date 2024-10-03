import sqlite3

'''def register(username: str, password: str) -> None:
    with sqlite3.connect('homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')
            """
        )
        conn.commit()'''
def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO table_users (username, password)
            VALUES (?, ?)
            """, (username, password)
        )
        conn.commit()


def hack() -> None:
    # Инъекция для удаления таблицы
    username: str = "hacker"
    password: str = "'); DROP TABLE table_users;--"
    register(username, password)

if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
