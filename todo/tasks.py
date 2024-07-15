from celery import shared_task
from django.core.mail import send_mail
from .models import TodoTask
from decouple import config

CELERY_EMAIL_SENDER=config('CELERY_EMAIL_SENDER')

@shared_task
def send_reminder_email(task_id):
    task = TodoTask.objects.get(id=task_id)
    send_mail(
        'Reminder for your Todo Task',
        f'Reminder: {task.name} is due soon. Please complete it before {task.deadline}.',
        f'{CELERY_EMAIL_SENDER}',  
        [task.user.email],  
        fail_silently=False,
    )
