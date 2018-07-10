from flask import current_app
from app import celery
from ... import mail

@celery.task
def my_background_task(arg1, arg2):
    result = 1000
    return result


@celery.task
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    app = current_app._get_current_object()
    with app.app_context():
        mail.send(msg)

@celery.task
def send_remote_task(task, args):
    task = celery.send_task(task, args)
