### Перед выполнением задания запустите файл generate_practice_and_homework_db.py!

Используя вложенные запросы найдите всех учеников того преподавателя, кто задает самые простые задания (те задания, где средний бал самый высокий)

* задание со звездочкой: напишите этот же запрос с использованием одного из join

SELECT s.full_name
FROM students s
JOIN assignments a ON s.group_id = a.group_id
JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
WHERE a.teacher_id = (
    SELECT teacher_id
    FROM assignments a
    JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
    GROUP BY a.teacher_id
    ORDER BY AVG(ag.grade) DESC
    LIMIT 1
);
