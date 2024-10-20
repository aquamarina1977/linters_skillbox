### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Используя подзапросы выведите среднюю оценку тех заданий, где ученикам нужно было что-то прочитать и выучить

SELECT AVG(ag.grade) AS avg_grade
FROM assignments_grades ag
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
WHERE a.assignment_text LIKE '%прочитать%' OR a.assignment_text LIKE '%выучить%';
