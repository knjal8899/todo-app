from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TodoTask
from tasks import send_reminder_email

class TodoTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoTask
        fields = ['id', 'created_at', 'modified_at', 'name', 'description', 'deadline']
    
    def create(self, validated_data):
        task = TodoTask.objects.create(**validated_data)
        if task.remind_at:
            send_reminder_email.apply_async(args=[task.id], eta=task.remind_at - timedelta(minutes=15))
        return task

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.remind_at = validated_data.get('remind_at', instance.remind_at)
        instance.save()
        if instance.remind_at:
            send_reminder_email.apply_async(args=[instance.id], eta=instance.remind_at - timedelta(minutes=15))
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
