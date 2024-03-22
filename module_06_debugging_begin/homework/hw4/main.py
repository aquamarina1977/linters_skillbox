"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
from typing import Dict
import logging
import json
import re

# Конфигурируем логгер
logging.basicConfig(filename='skillbox_json_messages.log', level=logging.INFO, format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')

class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # Экранируем кавычки в сообщении
        escaped_msg = json.dumps(msg)[1:-1]
        return escaped_msg, kwargs

# Создаем логгер с адаптером
logger = JsonAdapter(logging.getLogger(__name__))

# Пример использования
logger.warning('Сообщение со "словом" в кавычках')


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    d = {}
    with open('skillbox_json_messages.log', 'r') as file:
        d = {}
        with open('skillbox_json_messages.log', 'r') as file:
            for line in file:
                data = json.loads(line)
                level = data["level"]
                d[level] = d.get(level, 0) + 1
        return d

def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    d = {}
    with open('skillbox_json_messages.log', 'r', encoding='utf8') as file:
        for line in file:
            log_data = json.loads(line)
            log_time = log_data['time']
            log_hour = log_time.split(':')[0]
            d[log_hour] = d.get(log_hour, 0) + 1
        max_occurrences_hour = max(d, key=d.get)
        return int(max_occurrences_hour)

def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    with open('skillbox_json_messages.log', 'r') as file:
        logs = file.readlines()

    count_critical_logs = 0

    for log in logs:
        log_data = json.loads(log)
        log_time = log_data["time"]

        if "CRITICAL" in log_data["level"] and "05:00:00" <= log_time <= "05:20:00":
            count_critical_logs += 1

    return count_critical_logs


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    count = 0
    with open('skillbox_json_messages.log', 'r') as file:
        for line in file:
            entry = json.loads(line)
            if 'dog' in entry['message']:
                count += 1
    return count


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    word_count = {}

    with open('skillbox_json_messages.log', 'r') as file:
        for line in file:
            if '"level": "WARNING"' in line:
                message = re.search('"message": "(.*?)"', line).group(1)
                words = re.findall(r'\b\w+\b', message)
                for word in words:
                    word_count[word] = word_count.get(word, 0) + 1

    if word_count:
        most_common_word = max(word_count, key=word_count.get)
        return most_common_word

if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')

