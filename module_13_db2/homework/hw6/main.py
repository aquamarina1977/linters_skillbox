import sqlite3

TRAINING_SCHEDULE = {
    'Monday': 'Футбол',
    'Tuesday': 'Хоккей',
    'Wednesday': 'Шахматы',
    'Thursday': 'SUP-сёрфинг',
    'Friday': 'Бокс',
    'Saturday': 'Dota2',
    'Sunday': 'Шахбокс'
}

TRAINING_DAYS = {
    'Футбол': 'Monday',
    'Хоккей': 'Tuesday',
    'Шахматы': 'Wednesday',
    'SUP-сёрфинг': 'Thursday',
    'Бокс': 'Friday',
    'Dota2': 'Saturday',
    'Шахбокс': 'Sunday'
}

def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    cursor.execute("SELECT employee_id, date FROM table_friendship_schedule")
    schedule = cursor.fetchall()
    cursor.execute("SELECT id, preferable_sport FROM table_friendship_employees")
    employees_sports = cursor.fetchall()
    employee_to_sport = {emp_id: sport for emp_id, sport in employees_sports}
    updated_schedule = []
    for employee_id, work_day in schedule:
        sport = employee_to_sport.get(employee_id)
        if sport:
            training_day = TRAINING_DAYS.get(sport)
            if training_day and training_day == work_day:
                continue
        updated_schedule.append((employee_id, work_day))
    cursor.execute("DELETE FROM table_friendship_schedule")
    cursor.executemany("""
        INSERT INTO table_friendship_schedule (employee_id, date)
        VALUES (?, ?)
    """, updated_schedule)


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
