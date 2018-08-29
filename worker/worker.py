import time
import boto3
import json
from botocore.exceptions import ClientError
from celery import Celery

CELERY_BROKER_URL = 'amqp://myuser:mypassword@localhost:5672/myvhost'
CELERY_RESULT_BACKEND = 'amqp://myuser:mypassword@localhost:5672/myvhost'
CELERY_ACCEPT_CONTENT = ['pickle']
AWS_REGION = 'us-east-1'
CHARSET = 'UTF-8'
SENDER = 'no-reply@conferency.com'
client = boto3.client('ses', region_name=AWS_REGION)

app = Celery('worker', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.conf.update(accept_content=CELERY_ACCEPT_CONTENT)


@app.task(bind=True)
def long_task(self, iteration):
    for i in range(1, iteration):
        time.sleep(1)
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': iteration,
                                'status': str(i) + '%'})
    return {'current': 100, 'total': 100, 'status': '100%'}


@app.task(bind=True)
def send_email(self, email_json):
    email_json = json.loads(email_json)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    email_json['recipient'],
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': email_json['html'],
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': email_json['text'],
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': email_json['subject'],
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response)
    else:
        print('Email sent! Message ID:'),
        print(response['MessageId'])
