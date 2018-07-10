from celery import Celery
import time

CELERY_BROKER_URL = 'amqp://myuser:mypassword@localhost:5672/myvhost'
CELERY_RESULT_BACKEND = 'amqp://myuser:mypassword@localhost:5672/myvhost'

app = Celery('worker', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@app.task(bind=True)
def long_task(self, iteration):
    for i in range(1, iteration):
        time.sleep(1)
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': iteration,
                                'status': str(i) + '%'})
    return {'current': 100, 'total': 100, 'status': '100%'}
