from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_app.settings')

app = Celery('todo_app')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-reminder-emails-every-minute': {
        'task': 'todo.tasks.send_reminder_emails',
        'schedule': crontab(minute='*'), 
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
