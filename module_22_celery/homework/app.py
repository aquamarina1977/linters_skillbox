from flask import Flask, request, jsonify
from celery import group
from tasks import blur_image_task, revoke_weekly_email, send_weekly_email, send_images_email
from celery_app import celery
import os
import uuid

app = Flask(__name__)

@app.route('/blur', methods=['POST'])
def blur_images():
    images = request.json.get('images')
    email = request.json.get('email')

    if not images or not email or not isinstance(images, list):
        return jsonify({'error': 'Invalid images or email parameter'}), 400

    task_group = group(
        blur_image_task.s(image_path, f"blurred_{uuid.uuid4().hex}_{os.path.basename(image_path)}")
        for image_path in images
    )
    result = task_group.apply_async()

    if result:
        result.save()
        send_images_email.apply_async((result.id, email), countdown=5)
        return jsonify({'task_id': result.id}), 202
    else:
        return jsonify({'error': 'Failed to initiate image processing'}), 500


@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    result = celery.GroupResult.restore(task_id)
    if result is not None:
        completed_tasks = result.completed_count()
        total_tasks = len(result)
        progress = (completed_tasks / total_tasks) * 100 if total_tasks else 0
        status = 'completed' if result.ready() else 'processing'

        return jsonify({
            'status': status,
            'progress': f"{progress:.2f}%"
        }), 200
    else:
        return jsonify({'error': 'Invalid task ID'}), 404


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    if email:
        send_weekly_email.apply_async(args=[email])
        return jsonify({'message': 'Subscribed successfully'}), 200
    return jsonify({'error': 'Invalid email parameter'}), 400


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.json.get('email')
    if email:
        revoke_weekly_email.apply_async(args=[email])
        return jsonify({'message': 'Unsubscribed successfully'}), 200
    return jsonify({'error': 'Invalid email parameter'}), 400
