from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TodoTask
from .tasks import send_reminder_email
from todo_app.constants import REMINDER_TIME_DELTA


class TodoTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoTask
        fields = "__all__"

    def create(self, validated_data):
        task = TodoTask.objects.create(**validated_data)
        if task.deadline_ts:
            send_reminder_email.apply_async(args=[task.id], eta=task.deadline_ts - REMINDER_TIME_DELTA)
        return task

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.deadline_ts = validated_data.get('deadline_ts', instance.deadline_ts)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()
        if instance.deadline_ts:
            send_reminder_email.apply_async(args=[instance.id], eta=instance.deadline_ts - REMINDER_TIME_DELTA)
        return instance


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
