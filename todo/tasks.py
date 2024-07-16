from celery import shared_task
from django.utils import timezone
from .models import TodoTask
from .utils import send_reminder_email  
from todo_app.constants import REMINDER_TIME_DELTA

@shared_task
def send_reminder_emails():
    now = timezone.now()
    reminder_time_threshold = now + REMINDER_TIME_DELTA
    tasks_due_soon = TodoTask.objects.filter()
    for task in tasks_due_soon:
        send_reminder_email(task)
