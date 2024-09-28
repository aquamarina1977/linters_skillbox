## Задача 4. Исследование доходов населения
### Что нужно сделать
Представьте, что вы работаете в отделе статистики и учёта островного государства N. Вам поступило задание на крупное исследование касаемо доходов населения.

С помощью работы БД из Python вам нужно выполнить следующие задания:

1. Выяснить, сколько человек с острова N находятся за чертой бедности, то есть получает меньше 5000 гульденов в год.
2. Посчитать среднюю зарплату по острову N.
3. Посчитать медианную зарплату по острову. 
4. Посчитать число социального неравенства F, определяемое как `F = T/K`, где `T` — суммарный доход 10% самых обеспеченных жителей острова `N, K` — суммарный доход остальных 90% людей. Вывести ответ в процентах с точностью до двух знаков после запятой.

Обезличенную БД жителей острова N вы можете найти в файле `hw_4_database.db`. В таблице `salaries` находятся уникальные идентификаторы людей и их заработные платы.

_Опционально_. Для решения задачи 4 используйте только один SQL-запрос.

### Советы и рекомендации
* Медианная зарплата — это величина, которая делит население на две равные части: 50% получают зарплату ниже этого значения и 50% — выше.
* Для решения пригодятся функции [AVG](https://www.sqlitetutorial.net/sqlite-avg/), [SUM](https://www.sqlitetutorial.net/sqlite-sum/), [ROUND](https://www.sqlitetutorial.net/sqlite-functions/sqlite-round/) и [CAST](https://www.w3schools.com/sql/func_sqlserver_cast.asp).
* Чтобы составить сложный SQL-запрос, разложите его на более простые. Например, для решения опционального задания разложение может выглядеть так:
  * `SELECT 100 * ROUND(X / Y, 2)`
  * `X = SELECT SUM(salary) FROM TOP10`
  * `TOP10 = SELECT SUM(salary) FROM salaries ORDER BY salary DESC LIMIT 0.1 * TOTAL` 
  * `TOTAL = SELECT COUNT(salary) FROM salaries`
  * и так далее.

### Что оценивается
* Для получения количества, суммы или среднего арифметического используются соответствующие SQL-выражения.
* Ответ на задачу 4 имеет процентный формат с округлением до двух знаков после запятой.

Выяснить, сколько человек с острова N находятся за чертой бедности, то есть получает меньше 5000 гульденов в год.
WITH cte AS (SELECT salary
FROM salaries
WHERE salary < 5000)
SELECT COUNT(*) AS cnt
FROM cte;
Результат работы скрипта:
cnt: 5103;

Посчитать среднюю зарплату по острову N.
SELECT ROUND(AVG(salary), 2) AS avg_salary
FROM salaries;
Результат работы скрипта:
avg salary: 15426.32;

Посчитать медианную зарплату по острову.
WITH sorted_salaries AS (
    SELECT salary
    FROM salaries
    ORDER BY salary
)
SELECT 
    salary AS median_salary
FROM sorted_salaries
LIMIT 1 OFFSET (SELECT COUNT(*) FROM salaries) / 2;
Результат работы скрипта:
median salary: 15225;

Посчитать число социального неравенства F, определяемое как `F = T/K`, где `T` — суммарный доход 10% самых обеспеченных жителей острова `N, K` — суммарный доход остальных 90% людей. Вывести ответ в процентах с точностью до двух знаков после запятой.
Разложим задачу на простые подзапросы:
SELECT COUNT(salary) AS total FROM salaries;

SELECT SUM(salary) AS top_10_sum 
FROM salaries 
ORDER BY salary DESC 
LIMIT (SELECT COUNT(salary) * 0.1 FROM salaries);
Результат работы скрипта: 1130286106;

WITH top_10_cutoff AS (
    SELECT salary
    FROM salaries
    ORDER BY salary DESC
    LIMIT 1 OFFSET (SELECT COUNT(salary) * 0.1 FROM salaries) - 1
)
SELECT SUM(salary) AS bottom_90_sum
FROM salaries
WHERE salary < (SELECT salary FROM top_10_cutoff);
Результат работы скрипта: 923479420;

Находим индекс неравенства: 1.22;
