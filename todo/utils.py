from django.core.mail import send_mail
from django.conf import settings

def send_reminder_email(task):
    subject = 'Reminder: Task Due Soon'
    message = f'This is a reminder for your task "{task.name}". It is due on {task.deadline_ts}.'
    recipient_list = [task.user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
