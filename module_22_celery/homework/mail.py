'''import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT

def send_email(subject, recipient_email, attachment_path):
    try:

        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = recipient_email
        msg['Subject'] = subject

        body = "Please find the attached zip file with the processed images."
        msg.attach(MIMEText(body, 'plain'))

        with open(attachment_path, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name="processed_images.zip")
            part['Content-Disposition'] = f'attachment; filename="processed_images.zip"'
            msg.attach(part)

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"Email sent successfully to {recipient_email} with attachment {attachment_path}")
    except Exception as e:
        print(f"Failed to send email: {e}")'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT

def send_email(subject, recipient_email, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = recipient_email
        msg['Subject'] = subject

        body = "Please find the attached zip file with the processed images."
        msg.attach(MIMEText(body, 'plain'))

        # Открываем файл и добавляем в письмо
        with open(attachment_path, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name="processed_images.zip")
            part['Content-Disposition'] = 'attachment; filename="processed_images.zip"'
            msg.attach(part)

        # Подключаемся к серверу и отправляем письмо
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, recipient_email, msg.as_string())

        print(f"✅ Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

'''import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT

def send_email(subject, recipient_email, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = recipient_email
        msg['Subject'] = subject

        body = "Please find the attached zip file with the processed images."
        msg.attach(MIMEText(body, 'plain'))

        # Открываем файл и прикрепляем
        with open(attachment_path, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name="processed_images.zip")
            part['Content-Disposition'] = 'attachment; filename="processed_images.zip"'
            msg.attach(part)

        # Подключаемся через SSL (Яндекс требует этого)
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, recipient_email, msg.as_string())

        print(f"✅ Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT

def send_email(subject, recipient_email, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = recipient_email
        msg['Subject'] = subject

        body = "Please find the attached zip file with the processed images."
        msg.attach(MIMEText(body, 'plain'))

        with open(attachment_path, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name="processed_images.zip")
            part['Content-Disposition'] = f'attachment; filename="processed_images.zip"'
            msg.attach(part)

        # Подключаемся через SSL, а не через starttls()
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent successfully to {recipient_email} with attachment {attachment_path}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")'''





