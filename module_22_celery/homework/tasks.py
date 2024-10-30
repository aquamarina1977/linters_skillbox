import os
import zipfile
from celery_app import celery
from image import blur_image
from mail import send_email


@celery.task
def blur_image_task(src_filename, dst_filename):
    """Задача для размывания изображения."""
    try:
        blur_image(src_filename, dst_filename)
        return dst_filename
    except Exception as e:
        print(f"Error processing image {src_filename}: {e}")
        return None


@celery.task
def send_images_email(group_id, email):
    """Задача для создания архива и отправки email с обработанными изображениями."""
    result = celery.GroupResult.restore(group_id)
    if not result or not result.ready():
        print("Tasks are not complete yet.")
        return

    zip_filename = os.path.join("uploads", f"blurred_images_{group_id}.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for res in result.results:
            if res.successful():
                image_path = os.path.join("uploads", res.result)
                if os.path.exists(image_path):
                    zipf.write(image_path, os.path.basename(image_path))
                else:
                    print(f"Image {image_path} not found.")

    send_email(f"Blurred Images Order {group_id}", email, zip_filename)
    os.remove(zip_filename)

@celery.task
def send_weekly_email(email):
    send_email('Weekly Update', email, 'newsletter.pdf')

@celery.task
def revoke_weekly_email(email):
    print(f"User {email} has unsubscribed from the newsletter.")

