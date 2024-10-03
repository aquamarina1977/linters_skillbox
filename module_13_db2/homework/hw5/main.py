import sqlite3
import random

LEVELS = ['Сильная', 'Средняя', 'Средняя', 'Слабая']

COUNTRIES = [
    'Испания', 'Германия', 'Франция', 'Италия', 'Англия', 'Португалия',
    'Нидерланды', 'Бельгия', 'Хорватия', 'Швеция', 'Дания', 'Польша',
    'Швейцария', 'Япония', 'Россия', 'Австрия', 'Турция', 'Чехия'
]


def generate_team_name(country: str, level: str, count: int) -> str:
    """Генерация уникального имени команды."""
    return f'{country} {level} Команда {count}'


def generate_test_data(cursor: sqlite3.Cursor, number_of_groups: int) -> None:
    if number_of_groups < 4 or number_of_groups > 16:
        raise ValueError("Количество групп должно быть от 4 до 16.")
    cursor.execute("DELETE FROM uefa_commands")
    cursor.execute("DELETE FROM uefa_draw")
    teams_data = []
    draw_data = []
    country_count = 0
    for group_number in range(1, number_of_groups + 1):
        random.shuffle(LEVELS)
        for i, level in enumerate(LEVELS):
            country = COUNTRIES[country_count % len(COUNTRIES)]
            country_count += 1
            team_name = generate_team_name(country, level, country_count)
            teams_data.append((country_count, team_name, country, level))
            draw_data.append((country_count, group_number))
    cursor.executemany("""
        INSERT INTO uefa_commands (command_number, command_name, command_country, command_level)
        VALUES (?, ?, ?, ?)
    """, teams_data)
    cursor.executemany("""
        INSERT INTO uefa_draw (command_number, group_number)
        VALUES (?, ?)
    """, draw_data)


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()

    print("Данные успешно сгенерированы и добавлены в базы данных.")
