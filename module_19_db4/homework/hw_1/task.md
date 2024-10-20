### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Узнайте кто из преподавателей задает самые сложные задания. Иначе говоря задания какого преподавателя получают в среднем самые худшие оценки

SELECT t.full_name
FROM teachers t JOIN assignments a ON t.teacher_id = a.teacher_id 
JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id 
GROUP BY t.full_name 
ORDER BY AVG(grade)
LIMIT 1;