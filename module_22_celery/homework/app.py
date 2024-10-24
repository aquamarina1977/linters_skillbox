from celery.result import AsyncResult
from flask import Flask, request, jsonify
from celery.result import GroupResult
from celery import group
from celery import Celery
from celery.schedules import crontab
from image import blur_image
from mail import send_email
from config import SMTP_USER, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT

app = Flask(__name__)
app.config.update(
    broker_url='redis://localhost:6381/0',
    result_backend='redis://localhost:6381/0',
    task_result_expires=3600,
    result_persistent=True,
    smtp_user=SMTP_USER,
    smtp_host=SMTP_HOST,
    smtp_password=SMTP_PASSWORD,
    smtp_port=SMTP_PORT
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
            'args': ('example@example.com',)
        }
    }
    return celery

celery = make_celery(app)

@app.route('/blur', methods=['POST'])
def blur_images():
    images = request.files.getlist('images')
    email = request.form['email']
    task_group = group(
        blur_image_task.s(image.filename) for image in images
    )()
    return jsonify({'task_id': task_group.id}), 202


@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    group_result = GroupResult.restore(task_id)
    if not group_result:
        return jsonify({'status': 'Task ID not found'}), 404
    completed_tasks = group_result.completed_count()
    total_tasks = len(group_result)
    return jsonify({
        'status': 'in_progress' if not group_result.ready() else 'completed',
        'progress': f'{completed_tasks}/{total_tasks}'
    })


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
def send_weekly_email(email):
    send_email('weekly', email, 'newsletter.pdf')

@celery.task
def revoke_weekly_email(email):
    print(f"Пользователь {email} отписан от рассылки.")

if __name__ == '__main__':
    app.run(debug=True)
