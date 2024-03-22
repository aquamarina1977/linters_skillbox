"""
Удобно сохранять логи в определённом формате, чтобы затем их можно было фильтровать и анализировать. 
Сконфигурируйте логгер так, чтобы он писал логи в файл skillbox_json_messages.log в следующем формате:

{"time": "<время>", "level": "<уровень лога>", "message": "<сообщение>"}

Но есть проблема: если в message передать двойную кавычку, то лог перестанет быть валидной JSON-строкой:

{"time": "21:54:15", "level": "INFO", "message": "“"}

Чтобы этого избежать, потребуется LoggerAdapter. Это класс из модуля logging,
который позволяет модифицировать логи перед тем, как они выводятся.
У него есть единственный метод — process, который изменяет сообщение или именованные аргументы, переданные на вход.

class JsonAdapter(logging.LoggerAdapter):
  def process(self, msg, kwargs):
    # меняем msg
    return msg, kwargs

Использовать можно так:

logger = JsonAdapter(logging.getLogger(__name__))
logger.info('Сообщение')

Вам нужно дописать метод process так, чтобы в логах была всегда JSON-валидная строка.
"""

import logging
import re
def is_strong_password(password):
    dictionary = set()

    with open('/usr/share/dict/words', 'r') as file:
        for line in file:
            word = line.strip()
            if len(word) > 4:
                dictionary.add(word.lower())

    words = re.findall(r'\w{5,}', password.lower())

    for word in words:
        if word in dictionary:
            logger.error(f"Ненадлежащий пароль, содержит английское слово")
            return False
    logger.info("Сильный пароль")
    return True

class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        new_message = msg
        return new_message, kwargs


if __name__ == '__main__':

    logger = JsonAdapter(logging.getLogger(__name__))
    logger.setLevel(logging.DEBUG)
    logger.info('Сообщение')
    logger.error('Кавычка)"')
    logger.debug("Еще одно сообщение")

    password = "SecurePa****rd"
    is_strong_password(password)



