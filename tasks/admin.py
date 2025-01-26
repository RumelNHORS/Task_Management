from django.contrib import admin
from  tasks import models as tasks_models


admin.site.register(tasks_models.Task)
