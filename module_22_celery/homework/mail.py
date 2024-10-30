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

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"Email sent successfully to {recipient_email} with attachment {attachment_path}")
    except Exception as e:
        print(f"Failed to send email: {e}")
