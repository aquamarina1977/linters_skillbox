import sqlite3

IVAN_SALARY = 50000
def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    cursor.execute("""
            SELECT salary 
            FROM table_effective_manager 
            WHERE name LIKE ?
        """, (name,))
    result = cursor.fetchone()
    if result is None:
        print(f"Сотрудник с именем {name} не найден.")
        return
    employee_salary = result[0]
    new_salary = employee_salary * 1.10
    if new_salary > IVAN_SALARY:
        cursor.execute("""
                DELETE FROM table_effective_manager 
                WHERE name LIKE ?
            """, (name,))
        print(f"Сотрудник {name} уволен, так как его зарплата превышает зарплату Ивана Совина.")
    else:
        # Если не больше — повышаем зарплату
        cursor.execute("""
                UPDATE table_effective_manager
                SET salary = ?
                WHERE name LIKE ?
            """, (new_salary, name))
        print(f"Зарплата сотрудника {name} была увеличена до {new_salary}.")


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
