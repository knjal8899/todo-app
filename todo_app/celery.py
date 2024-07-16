from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_app.settings')

app = Celery('todo_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-reminder-every-hour': {
        'task': 'todo_app.tasks.send_reminder_email',
        'schedule': crontab(minute=0, hour='*/1'), 
        'args': (1,),  
    },
    
}

app.autodiscover_tasks()