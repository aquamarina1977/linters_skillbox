### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Используя вложенные запросы посчитайте среднее, макс и мин количество просроченных заданий для каждого класса.

* задание со звездочкой: напишите этот же запрос с использованием одного из join

SELECT group_id,
       AVG(overdue_count) AS avg_overdue,
       MAX(overdue_count) AS max_overdue,
       MIN(overdue_count) AS min_overdue
FROM (
    SELECT group_id,
           COUNT(*) AS overdue_count
    FROM assignments a
    JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
    WHERE ag.date > a.due_date
    GROUP BY a.group_id
) AS overdue_stats
GROUP BY group_id;

* Задание со звёздочкой:
SELECT g.group_id,
       AVG(overdue.overdue_count) AS avg_overdue,
       MAX(overdue.overdue_count) AS max_overdue,
       MIN(overdue.overdue_count) AS min_overdue
FROM students_groups g
JOIN (
    SELECT group_id,
           COUNT(*) AS overdue_count
    FROM assignments a
    JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
    WHERE ag.date > a.due_date
    GROUP BY a.group_id
) overdue ON g.group_id = overdue.group_id
GROUP BY g.group_id;