from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import json

from .models import Todo

class TodoModelTests(TestCase):
    def test_todo_creation(self):
        """Test creating a new todo"""
        todo = Todo.objects.create(
            title="Test Task",
            description="Test Description",
            priority="high"
        )
        self.assertEqual(todo.title, "Test Task")
        self.assertEqual(todo.priority, "high")
        self.assertFalse(todo.completed)
        
    def test_todo_str_representation(self):
        """Test string representation of todo"""
        todo = Todo.objects.create(title="Test Task")
        self.assertEqual(str(todo), "Test Task")
        
    def test_is_overdue_property(self):
        """Test the is_overdue property"""
        # Future due date - not overdue
        future_todo = Todo.objects.create(
            title="Future Task",
            due_date=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(future_todo.is_overdue)
        
        # Past due date - overdue
        past_todo = Todo.objects.create(
            title="Past Task",
            due_date=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(past_todo.is_overdue)
        
        # Completed task - not overdue even if past due
        completed_todo = Todo.objects.create(
            title="Completed Task",
            due_date=timezone.now() - timedelta(days=1),
            completed=True
        )
        self.assertFalse(completed_todo.is_overdue)
        
    def test_priority_icon_property(self):
        """Test priority icon property"""
        high_todo = Todo.objects.create(title="High", priority="high")
        medium_todo = Todo.objects.create(title="Medium", priority="medium")
        low_todo = Todo.objects.create(title="Low", priority="low")
        
        self.assertEqual(high_todo.priority_icon, "🔴")
        self.assertEqual(medium_todo.priority_icon, "🟡")
        self.assertEqual(low_todo.priority_icon, "🟢")

class TodoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Test Task",
            description="Test Description",
            priority="medium"
        )
        
    def test_todo_form_view(self):
        """Test the main todo form view"""
        response = self.client.get(reverse('example_app:todo_form'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task Master")
        self.assertContains(response, "Test Task")
        
    def test_todo_list_view(self):
        """Test the todo list view"""
        response = self.client.get(reverse('example_app:todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task List")
        
    def test_dashboard_view(self):
        """Test the dashboard view"""
        response = self.client.get(reverse('example_app:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")
        
    def test_create_todo(self):
        """Test creating a new todo via POST"""
        response = self.client.post(reverse('example_app:todo_form'), {
            'title': 'New Task',
            'description': 'New Description',
            'priority': 'high'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Todo.objects.filter(title='New Task').exists())
        
    def test_toggle_todo(self):
        """Test toggling todo completion status"""
        self.assertFalse(self.todo.completed)
        
        response = self.client.post(reverse('example_app:toggle_todo', args=[self.todo.id]))
        self.assertEqual(response.status_code, 302)
        
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)
        
    def test_delete_todo(self):
        """Test deleting a todo"""
        todo_id = self.todo.id
        response = self.client.post(reverse('example_app:delete_todo', args=[todo_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(id=todo_id).exists())
        
    def test_todo_stats_api(self):
        """Test the todo statistics API"""
        response = self.client.get(reverse('example_app:todo_stats_api'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('total', data)
        self.assertIn('completed', data)
        self.assertIn('pending', data)
        self.assertEqual(data['total'], 1)
        
    def test_bulk_action_api_complete_all(self):
        """Test bulk action API for completing tasks"""
        # Create additional tasks
        Todo.objects.create(title="Task 2", priority="low")
        Todo.objects.create(title="Task 3", priority="high")
        
        response = self.client.post(
            reverse('example_app:bulk_action_api'),
            data=json.dumps({
                'action': 'complete_all',
                'todo_ids': []  # Empty list should complete all pending
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # Check that all todos are now completed
        completed_count = Todo.objects.filter(completed=True).count()
        self.assertEqual(completed_count, 3)
        
    def test_bulk_action_api_invalid_action(self):
        """Test bulk action API with invalid action"""
        response = self.client.post(
            reverse('example_app:bulk_action_api'),
            data=json.dumps({
                'action': 'invalid_action',
                'todo_ids': [self.todo.id]
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid action')

class TodoFormTests(TestCase):
    def test_valid_form_data(self):
        """Test form with valid data"""
        from .forms import TodoForm
        
        form_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'high',
            'completed': False
        }
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_form_missing_required_field(self):
        """Test form with missing required field"""
        from .forms import TodoForm
        
        form_data = {
            'description': 'Test Description',
            'priority': 'high'
        }
        form = TodoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        
    def test_form_saves_correctly(self):
        """Test that form saves data correctly"""
        from .forms import TodoForm
        
        form_data = {
            'title': 'Form Test Task',
            'description': 'Form Test Description',
            'priority': 'medium',
            'completed': True
        }
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        todo = form.save()
        self.assertEqual(todo.title, 'Form Test Task')
        self.assertEqual(todo.priority, 'medium')
        self.assertTrue(todo.completed)

class URLTests(TestCase):
    def test_url_patterns(self):
        """Test that all URL patterns resolve correctly"""
        # Create a test todo for URLs that need an ID
        todo = Todo.objects.create(title="Test Task")
        
        urls_to_test = [
            ('example_app:todo_form', []),
            ('example_app:todo_list', []),
            ('example_app:dashboard', []),
            ('example_app:toggle_todo', [todo.id]),
            ('example_app:delete_todo', [todo.id]),
            ('example_app:todo_stats_api', []),
            ('example_app:bulk_action_api', []),
        ]
        
        for url_name, args in urls_to_test:
            with self.subTest(url_name=url_name):
                url = reverse(url_name, args=args)
                self.assertIsNotNone(url)
                # Basic GET request test (except for POST-only endpoints)
                if url_name not in ['example_app:bulk_action_api']:
                    response = self.client.get(url)
                    self.assertIn(response.status_code, [200, 302, 405])  # 405 for POST-only views
