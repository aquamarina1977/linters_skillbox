from flask import Flask, request, jsonify
from celery import Celery, group
from celery.schedules import crontab
from image import blur_image
from mail import send_email
import zipfile
import os

app = Flask(__name__)

app.config.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_result_expires=3600,
    result_persistent=True,
    redis_max_connections=20
)


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['broker_url'],
        backend=app.config['result_backend']
    )
    celery.conf.update(app.config)
    celery.conf.beat_schedule = {
        'send-weekly-newsletter': {
            'task': 'send_weekly_email',
            'schedule': crontab(day_of_week=0, hour=8, minute=0),
            'args': ('weekly@newsletter.com',)
        }
    }
    return celery


celery = make_celery(app)


@app.route('/blur', methods=['POST'])
def blur_images():
    images = request.json.get('images')
    email = request.json.get('email')

    if not images or not email or not isinstance(images, list):
        return jsonify({'error': 'Invalid images or email parameter'}), 400

    task_group = group(
        blur_image_task.s(image_path) for image_path in images
    )
    result = task_group.apply_async()

    result.save()

    send_images_email.apply_async((result.id, email), countdown=5)
    return jsonify({'task_id': result.id}), 202


@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    result = celery.GroupResult.restore(task_id)
    if result:
        progress = result.completed_count() / len(result) * 100
        status = 'completed' if result.ready() else 'processing'
        return jsonify({'status': status, 'progress': f"{progress:.2f}%"}), 200
    else:
        return jsonify({'error': 'Invalid task ID'}), 404


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    send_weekly_email.apply_async(args=[email])
    return jsonify({'message': 'Subscribed successfully'}), 200


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.form['email']
    revoke_weekly_email.apply_async(args=[email])
    return jsonify({'message': 'Unsubscribed successfully'}), 200


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


if __name__ == '__main__':
    app.run(debug=True)
