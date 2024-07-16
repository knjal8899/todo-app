# todo/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from todo_app.constants import REMINDER_TIME_DELTA

@shared_task
def send_reminder_email(task_id):
    from .models import TodoTask
    try:
        task = TodoTask.objects.get(id=task_id)
        if task.remind_at <= now():  # Check if the reminder time has passed
            send_mail(
                'Task Reminder',
                f'Reminder for your task: {task.name}\nDescription: {task.description}\nDeadline: {task.deadline_ts}',
                'from@example.com',  # Update this to the sender's email address
                [task.user.email],
                fail_silently=False,
            )
    except TodoTask.DoesNotExist:
        pass

# Adding periodic tasks if needed:
from celery import Celery
from celery.schedules import crontab

app = Celery('todo_app')

app.conf.beat_schedule = {
    'send-reminder-email-every-hour': {
        'task': 'todo.tasks.send_reminder_email',
        'schedule': crontab(minute=0, hour='*'),  # Every hour
    },
}

# Ensure you have an instance of the Celery app loaded for configuration
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
