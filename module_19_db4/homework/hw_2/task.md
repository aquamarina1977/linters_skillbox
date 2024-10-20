### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Дирекция школы решила наградить лучших учеников грамотами, но вот беда, в принтере картриджа хватит всего на 10 бланков. Выберите 10 лучших учеников с лучшими оценками в сроеднем. Не забудьте отсортировать список в низходящем порядке
SELECT s.full_name
FROM students s JOIN assignments_grades ag ON s.student_id = ag.student_id 
GROUP BY s.full_name 
ORDER BY AVG(grade) DESC
LIMIT 10;