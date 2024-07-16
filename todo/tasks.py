

from celery import shared_task
from django.core.mail import send_mail
from django.http import Http404
from django.utils.timezone import now
from todo_app.constants import REMINDER_TIME_DELTA

@shared_task
def send_reminder_email(task_id):
    from .models import TodoTask
    try:
        task = TodoTask.objects.get(id=task_id)
        if task.remind_at <= now(): 
            send_mail(
                'Task Reminder',
                f'Reminder for your task: {task.name}\nDescription: {task.description}\nDeadline: {task.deadline_ts}',
                'from@example.com', 
                [task.user.email],
                fail_silently=False,
            )
    except TodoTask.DoesNotExist:
        raise Http404

