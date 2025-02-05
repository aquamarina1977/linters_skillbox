"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""

#'https://yandex.ru/support/mail/mail-clients/others.html'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

SMTP_USER = "m.shesterenko@yandex.ru"
SMTP_PASSWORD = "your_yandex_password"
SMTP_HOST = "smtp.yandex.ru"
SMTP_PORT = 587 # Используем SSL (если TLS, то порт 587)

