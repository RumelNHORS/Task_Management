from django.urls import path
from tasks import views as tasks_views


urlpatterns = [
    path('tasks/', tasks_views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', tasks_views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/overdue/', tasks_views.OverdueTaskView.as_view(), name='overdue-tasks'),
]
