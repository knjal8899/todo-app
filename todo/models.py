from django.db import models
from django.core.mail import send_mail 
from decouple import config

CELERY_EMAIL_SENDER = config('CELERY_EMAIL_SENDER')  

class TodoTask(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  

    def __str__(self):
        return self.name
    
    def send_reminder_email(self):
        send_mail(
            'Reminder for your Todo Task',
            f'Reminder: {self.name} is due soon. Please complete it before {self.deadline}.',
            f'{CELERY_EMAIL_SENDER}', 
            [self.user.email], 
            fail_silently=False,
        )
