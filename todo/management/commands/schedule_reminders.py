from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from todo.tasks import send_reminder_email
from todo.models import TodoTask

class Command(BaseCommand):
    help = 'Schedule reminder emails for tasks'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        tasks = TodoTask.objects.filter(remind_at__lte=now + timedelta(minutes=15))
        for task in tasks:
            send_reminder_email.apply_async(args=[task.id], countdown=task.remind_at - now)
        self.stdout.write(self.style.SUCCESS('Scheduled reminder emails for tasks.'))
