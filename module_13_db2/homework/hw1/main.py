import sqlite3


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    query = """
        SELECT EXISTS(
            SELECT 1
            FROM table_truck_with_vaccine
            WHERE truck_number = ?
            GROUP BY strftime('%Y-%m-%d %H', timestamp)
            HAVING SUM(CASE 
                          WHEN temperature_in_celsius NOT BETWEEN -20 AND -16 THEN 1 
                          ELSE 0 
                      END) >= 3
        );
        """
    cursor.execute(query, (truck_number,))
    return cursor.fetchone()[0] == 1


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
