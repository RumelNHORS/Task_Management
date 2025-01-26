from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.timezone import now
from tasks import models as tasks_models
from tasks import serializers as tasks_serializers


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = tasks_models.Task.objects.all()
    serializer_class = tasks_serializers.TaskSerializer

    def get_queryset(self):
        status_filter = self.request.query_params.get('status')
        if status_filter:
            return self.queryset.filter(status=status_filter)
        return self.queryset

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = tasks_models.Task.objects.all()
    serializer_class = tasks_serializers.TaskSerializer

class OverdueTaskView(generics.ListAPIView):
    queryset = tasks_models.Task.objects.filter(due_date__lt=now().date())
    serializer_class = tasks_serializers.TaskSerializer

