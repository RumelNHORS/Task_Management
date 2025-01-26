from django.urls import path
from tasks import views as tasks_views


urlpatterns = [

    # User register/login/logout
    path('register/', tasks_views.UserRegistrationView.as_view(), name='register'),
    path('login/', tasks_views.UserLoginView.as_view(), name='login'),
    path('logout/', tasks_views.UserLogoutView.as_view(), name='logout'),

    # Tasks creat/update/delete
    path('tasks/', tasks_views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', tasks_views.TaskDetailView.as_view(), name='task-detail'),
    # Overdue tasks
    path('tasks/overdue/', tasks_views.OverdueTaskView.as_view(), name='overdue-tasks'),
]
