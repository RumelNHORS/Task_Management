from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task
from django.contrib.auth.models import User
from datetime import date


class TaskAPITests(APITestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a task
        self.task = Task.objects.create(
            title='Test Task 1',
            description='Task description',
            status='Pending',
            due_date=date(2025, 1, 30)
        )
        
        # Create another task
        self.task2 = Task.objects.create(
            title='Test Task 2',
            description='Task description',
            status='Completed',
            due_date=date(2025, 1, 25)
        )
    
    def test_task_list_create(self):
        url = reverse('task-list-create')

        # Test GET request to list tasks
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We created 2 tasks
        
        # Test POST request to create a new task
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'status': 'Pending',
            'due_date': '2025-02-10',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
    
    def test_task_detail(self):
        url = reverse('task-detail', kwargs={'pk': self.task.pk})

        # Test GET request to retrieve a task
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task 1')

        # Test PATCH request to update a task
        data = {'status': 'In Progress'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'In Progress')

        # Test DELETE request to delete a task
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)  # Only task2 should remain
    
    def test_overdue_task_view(self):
        url = reverse('overdue-tasks')

        # Test GET request for overdue tasks
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only task2 is overdue
        
        # Ensure overdue task has the correct status
        self.assertEqual(response.data[0]['title'], 'Test Task 2')
    
    def test_filtered_task_list(self):
        url = reverse('task-list-create')
        
        # Test GET request to filter tasks by status
        response = self.client.get(url, {'status': 'Pending'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only task1 should be 'Pending'
        self.assertEqual(response.data[0]['title'], 'Test Task 1')
