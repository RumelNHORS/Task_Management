from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.utils.timezone import now
from tasks import models as tasks_models
from tasks import serializers as tasks_serializers
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class UserRegistrationView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = tasks_serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({
                "message": "Login successful!",
                "user": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
    

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = tasks_serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        status_filter = self.request.query_params.get('status')
        queryset = tasks_models.Task.objects.filter(user=self.request.user)
        if status_filter:
            # Use iexact for case-insensitive exact match
            queryset = queryset.filter(status__iexact=status_filter)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = tasks_serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return tasks_models.Task.objects.filter(user=self.request.user)

    def get_object(self):
        obj = get_object_or_404(tasks_models.Task, pk=self.kwargs["pk"])
        # Custom permission check
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to modify this task. Only the creator can update or delete it.")
        return obj


class OverdueTaskView(generics.ListAPIView):
    serializer_class = tasks_serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return tasks_models.Task.objects.filter(user=self.request.user, due_date__lt=now().date())

