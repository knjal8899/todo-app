import threading
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TodoTask
from .tasks import send_reminder_email
from todo_app.constants import REMINDER_TIME_DELTA
from concurrent.futures import ThreadPoolExecutor


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TodoTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoTask
        fields = "__all__"
        read_only_fields = ["user", "remind_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data.pop("user", None)
        task = TodoTask.objects.create(user=user, **validated_data)

        if task.deadline_ts:
            remind_at = task.deadline_ts - REMINDER_TIME_DELTA
            task.remind_at = remind_at
            task.save()
            threading.Thread(target=send_reminder_email, args=(task.id,)).start()

        return task

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.deadline_ts = validated_data.get("deadline_ts", instance.deadline_ts)
        instance.status = validated_data.get("status", instance.status)
        instance.priority = validated_data.get("priority", instance.priority)

        if instance.deadline_ts:
            remind_at = instance.deadline_ts - REMINDER_TIME_DELTA
            instance.remind_at = remind_at
            with ThreadPoolExecutor() as executor:
                executor.submit(send_reminder_email, instance.id)

        instance.save()
        return instance
