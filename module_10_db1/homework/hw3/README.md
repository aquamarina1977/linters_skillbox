## Задача 3. Анализ таблиц
### Что нужно сделать

Попрактикуемся в работе с БД из Python.

Есть база данных `hw_3_database.db`, в которой находятся три таблицы:
`table_1`, `table_2` и `table_3`. Каждая таблица имеет структуру из двух столбцов: `id` (число) и `value` (строка).

Выполните запросы, которые дадут ответы на следующие вопросы:

1. Сколько записей (строк) хранится в каждой таблице?
2. Сколько в таблице `table_1` уникальных записей?<br>Назовём уникальной такую запись, которая ранее не встречалась в таблице.
3. Как много записей из таблицы `table_1` встречается в `table_2`?
4. Как много записей из таблицы `table_1` встречается и в `table_2`, и в `table_3`?

### Советы и рекомендации
* Получить записи из таблицы можно так:
  ```python
  import sqlite3
  
  with sqlite3.connect("hw_3_database.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `some_database_table_name`")
    result = cursor.fetchall()
  ``` 
* Для получения уникальных записей можно воспользоваться [DISTINCT](https://www.sqlitetutorial.net/sqlite-distinct/).
* Если нужно ответить на вопрос «сколько?», необязательно получать из таблицы все строки. Достаточно добавить в SQL запрос [COUNT](https://www.sqlitetutorial.net/sqlite-count-function/).
* Для нахождения пересечения таблиц поможет [INTERSECT](https://www.sqlitetutorial.net/sqlite-intersect/) или [JOIN](https://www.sqlitetutorial.net/sqlite-join/).

### Что оценивается
* Python не производит никаких операций над полученными строками. В большей мере используются возможности SQL-запросов.
* Все запросы делаются в рамках одного подключения к БД.

Сколько записей (строк) хранится в каждой таблице?
SELECT COUNT(*) AS cnt
FROM table_1;
Результат выполения скрипта:
cnt: 2222;
SELECT COUNT(*) AS cnt
FROM table_2;
Результат выполнения скрипта:
cnt: 2999;
SELECT COUNT(*) AS cnt
FROM table_3;
Результат выполнения скрипта:
cnt: 3826;

Сколько в таблице table_1 уникальных записей?
WITH cte AS (SELECT DISTINCT value 
FROM table_1 t)
SELECT COUNT(*)
FROM cte;
Результат работы программы:
cnt: 2222;

Как много записей из таблицы table_1 встречается в таблице table_2?
SELECT COUNT(*)
FROM (
    SELECT *
    FROM table_1
    INTERSECT
    SELECT *
    FROM table_2
) AS result;
Результат работы програмы:
COUNT(*): 499;

Как много записей из таблицы table_1 встречается в таблице table_2 и table_3?
SELECT COUNT(*)
FROM (
    SELECT *
    FROM table_1
    INTERSECT
    SELECT *
    FROM table_2
    INTERSECT
    SELECT *
    FROM table_3
) AS result;
Результат работы скрипта:
COUNT(*): 326;