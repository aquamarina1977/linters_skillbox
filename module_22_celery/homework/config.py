"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""

# https://yandex.ru/support/mail/mail-clients/others.html

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

SMTP_USER = "seurat298@gmail.com"
SMTP_PASSWORD = "fitness1977landscape / fpsi qzeh rpws yusk"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
