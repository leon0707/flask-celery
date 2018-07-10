# -*- coding: utf-8 -*-

# from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from .. import mail


# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)


def generate_email(to, subject, template, reply_to=None,
               **kwargs):
    """Send email function."""
    app = current_app._get_current_object()
    msg = Message(subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to],
                  reply_to=reply_to)
    msg.body = render_template(
        template + '.txt', **kwargs)
    msg.html = render_template(
        template + '.html', **kwargs)
    return msg
    # thr = Thread(target=send_async_email, args=[app, msg])
    # thr.start()
    # return thr
