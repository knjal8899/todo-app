from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TodoTask
from .serializers import TodoTaskSerializer, UserSerializer


class RegisterUserView(APIView):
   
    def post(self, request):
        """         
        Register a new user.

        Request URL: `/api/v1/register/`

        Request Body:
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "newpassword"
            }

        Success Response:
            Status Code: 201 Created
            {
                "message": "User registered successfully!"
            }

        Failure Response:
            Status Code: 400 Bad Request
            {
                "email": ["This field is required."],
                "password": ["This field is required."],
                "username": ["This field is required."]
            }    

        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):

    def post(self, request):
        """
            
        User login.

        Request URL: `/api/v1/login/`

        Request Body:
            {
                "username": "testuser",
                "password": "testpassword"
            }

        Success Response:
            Status Code: 200 OK
            {
                "refresh": "JWT refresh token",
                "access": "JWT access token"
            }

        Failure Response:
            Status Code: 401 Unauthorized
            {
                "error": "Invalid credentials"
            }
        

        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class TodoTaskListView(APIView):
  
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List and create Todo tasks.

        URL: `/api/v1/tasks/`
            
        Success Response:
            Status Code: 200 OK
            {
                "data": [
                    {
                        "id": 1,
                        "created_at": "2023-01-01T12:00:00Z",
                        "modified_at": "2023-01-01T12:00:00Z",
                        "name": "Sample Task",
                        "description": "This is a sample task",
                        "deadline_ts": "2023-01-02T12:00:00Z",
                        "created_by": 1,
                        "report_to": 2,
                        "status": "TODO",
                        "is_deleted": false,
                        "priority": "MEDIUM"
                    }
                ]
            }
            
        Failure Response:
        Status Code: 400 Bad Request
        {
            "errors": {
                "field_name": ["Error message"]
            }
        }

        """
        tasks = TodoTask.objects.filter(is_deleted=False)
        serializer = TodoTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
         Request Body:
        {
            "name": "New Task",
            "description": "This is a new task",
            "deadline_ts": "2024-12-31T23:59:59Z",
            "report_to": 2,
            "status": "TODO",
            "priority": "MEDIUM"
        }

        Success Response:
            Status Code: 201 Created
            {
                "data": {
                    "id": 1,
                    "created_at": "2023-01-01T12:00:00Z",
                    "modified_at": "2023-01-01T12:00:00Z",
                    "name": "New Task",
                    "description": "This is a new task",
                    "deadline_ts": "2024-12-31T23:59:59Z",
                    "created_by": 1,
                    "report_to": 2,
                    "status": "TODO",
                    "is_deleted": false,
                    "priority": "MEDIUM"
                }
            }

        Failure Response:
            Status Code: 400 Bad Request
            {
                "errors": {
                    "field_name": ["Error message"]
                }
            }
        """
        serializer = TodoTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoTaskDetailView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        
        try:
            return TodoTask.objects.get(pk=pk, is_deleted=False)
        except TodoTask.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        URL: `/api/v1/tasks/<pk>/`

        Success Response:
            Status Code: 200 OK
            {
                "data": {
                    "id": 1,
                    "created_at": "2023-01-01T12:00:00Z",
                    "modified_at": "2023-01-01T12:00:00Z",
                    "name": "Sample Task",
                    "description": "This is a sample task",
                    "deadline_ts": "2023-01-02T12:00:00Z",
                    "created_by": 1,
                    "report_to": 2,
                    "status": "TODO",
                    "is_deleted": false,
                    "priority": "MEDIUM"
                }
            }
            
        Failure Response:
        Status Code: 404 Not Found
        {
            "error": "Task not found."
        }

        """
        task = self.get_object(pk)
        if not task:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoTaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        URL: `/api/v1/tasks/<pk>/`

        Request Body:
        {
            "name": "Updated Task",
            "description": "This is an updated task",
            "deadline_ts": "2025-01-01T23:59:59Z",
            "report_to": 2,
            "status": "INPROGRESS",
            "priority": "HIGH"
        }

        Success Response:
            Status Code: 200 OK
            {
                "data": {
                    "id": 1,
                    "created_at": "2023-01-01T12:00:00Z",
                    "modified_at": "2023-01-01T12:00:00Z",
                    "name": "Updated Task",
                    "description": "This is an updated task",
                    "deadline_ts": "2025-01-01T23:59:59Z",
                    "created_by": 1,
                    "report_to": 2,
                    "status": "INPROGRESS",
                    "is_deleted": false,
                    "priority": "HIGH"
                }
            }
        Failure Response:
            Status Code: 404 Not Found
            {
                "error": "Task not found."
            }

        """
        task = self.get_object(pk)
        if not task:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TodoTaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        URL: `/api/v1/tasks/<pk>/`
        
        Success Response:
            Status Code: 204 No Content
            {
                "message": "Task deleted successfully."
            }

        Failure Response:
            Status Code: 404 Not Found
            {
                "error": "Task not found."
            }
    
        
        """
        task = self.get_object(pk)
        if not task:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

        task.is_deleted = True
        task.save()
        return Response({'message': 'Task deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
