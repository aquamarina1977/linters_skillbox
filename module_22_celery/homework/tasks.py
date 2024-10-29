from image import blur_image
from mail import send_email
import zipfile
import os
from celery_app import celery

@celery.task
def blur_image_task(image_name, dst_filename):
    """Задача для размывания изображения через Celery."""
    src_path = os.path.join("uploads", image_name)
    dst_path = os.path.join("uploads", dst_filename)

    if not os.path.exists(src_path):
        print(f"Ошибка: Файл {src_path} не найден.")
        return None

    try:
        blur_image(src_path, dst_path)
        return dst_filename
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

@celery.task
def send_images_email(group_id, email):
    result = celery.GroupResult.restore(group_id)
    if not result or not result.successful():
        return

    zip_filename = os.path.join("uploads", f"blurred_images_{group_id}.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for res in result.children:
            if res.successful() and res.result:
                image_path = os.path.join("uploads", res.result)
                zipf.write(image_path, os.path.basename(image_path))

    send_email('Blurred Images', email, zip_filename)
    os.remove(zip_filename)

@celery.task
def send_weekly_email(email):
    send_email('Weekly Update', email, 'newsletter.pdf')

@celery.task
def revoke_weekly_email(email):
    print(f"User {email} has unsubscribed from the newsletter.")
