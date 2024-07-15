from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import TodoTask
from .serializers import TodoTaskSerializer

User = get_user_model()

class TodoAppTests(APITestCase):
    def setUp(self):
        # Create a dummy user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Log in to obtain a token
        response = self.client.post(reverse('login-user'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create a sample task
        self.task = TodoTask.objects.create(
            name='Test Task',
            description='This is a test task',
            deadline='2024-12-31T23:59:59Z'
        )
        self.task_url = reverse('task-detail', kwargs={'pk': self.task.pk})
        self.tasks_url = reverse('task-list')
        self.register_url = reverse('register-user')
        self.login_url = reverse('login-user')

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'password2': 'newpassword',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully!!')

    def test_login_user(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_list_todo_tasks(self):
        response = self.client.get(self.tasks_url, format='json')
        tasks = TodoTask.objects.all()
        serializer = TodoTaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_todo_task(self):
        data = {
            'name': 'New Task',
            'description': 'This is a new task',
            'deadline': '2024-12-31T23:59:59Z'
        }
        response = self.client.post(self.tasks_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Task')

    def test_get_todo_task(self):
        response = self.client.get(self.task_url, format='json')
        serializer = TodoTaskSerializer(self.task)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_todo_task(self):
        data = {
            'name': 'Updated Task',
            'description': 'This is an updated task',
            'deadline': '2025-01-01T23:59:59Z'
        }
        response = self.client.put(self.task_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Task')

    def test_delete_todo_task(self):
        response = self.client.delete(self.task_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TodoTask.objects.filter(pk=self.task.pk).exists())
