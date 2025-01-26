from rest_framework import serializers
from tasks import models as tasks_models



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = tasks_models.Task
        fields = '__all__'

