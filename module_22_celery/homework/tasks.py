from image import blur_image
from mail import send_email
import zipfile
import os
from celery_app import celery

@celery.task
def blur_image_task(image_path):
    dst_filename = f'blur_{image_path}'
    blur_image(image_path, dst_filename)
    return dst_filename


@celery.task
def send_images_email(group_id, email):
    result = celery.GroupResult.restore(group_id)
    if not result or not result.successful():
        return

    zip_filename = f"blurred_images_{group_id}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for image_path in result.get():
            zipf.write(image_path, os.path.basename(image_path))

    send_email('Blurred Images', email, zip_filename)

    os.remove(zip_filename)

@celery.task
def send_weekly_email(email):
    send_email('Weekly Update', email, 'newsletter.pdf')


@celery.task
def revoke_weekly_email(email):
    print(f"User {email} has unsubscribed from the newsletter.")