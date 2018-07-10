# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for, request, jsonify
from . import task
from .tasks import send_async_email, my_background_task
from app.utiles.email_operation import generate_email
from celery.execute import send_task
from celery.result import AsyncResult

@task.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        email = request.form['email']
        msg = generate_email(email, 'hello', 'emails/template')
        task = send_async_email.apply_async(args=[msg], countdown=60)
    my_background_task.delay(1, 1)
    return render_template('/task/send_email.html')


@task.route('/send_task/<int:i>', methods=['POST'])
def send_remote_task(i):
    task = send_task('worker.long_task', [i])
    return jsonify({'task_id': task.id})


@task.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    res = AsyncResult(task_id)
    if res.state == 'PENDING':
        response = {
            'state': res.state,
            'current': 0,
            'total': 0,
            'status': 'Pending...'
        }
    else:
        response = {
            'state': res.state,
            'current': res.info.get('current', 0),
            'total': res.info.get('total', 0),
            'status': res.info.get('status', 0)
        }
    return jsonify(response)
