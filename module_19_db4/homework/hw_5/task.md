### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Узнайте все про группы! Количество учеников, средняя оценка, сколько человек не сдали работы и сколько опоздали со задачей работы. И сколько в каждой группе было повторных попыток сдать работу.

SELECT g.group_id,
       COUNT(DISTINCT s.student_id) AS total_students,
       AVG(ag.grade) AS average_grade,
       SUM(CASE WHEN ag.grade IS NULL THEN 1 ELSE 0 END) AS missed_assignments,
       SUM(CASE WHEN ag.date > a.due_date THEN 1 ELSE 0 END) AS overdue_assignments,
       COUNT(DISTINCT ag.assisgnment_id) - COUNT(DISTINCT a.assisgnment_id) AS retry_count
FROM students_groups g
JOIN students s ON g.group_id = s.group_id
JOIN assignments a ON g.group_id = a.group_id
JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
GROUP BY g.group_id;
