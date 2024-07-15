from django.urls import path
from .views import RegisterUserView, LoginUserView, TodoTaskListView, TodoTaskDetailView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('tasks/', TodoTaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TodoTaskDetailView.as_view(), name='task-detail'),
]
