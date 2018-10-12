from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from autofixture import AutoFixture
from tasks.forms import TaskForm
from tasks.models import Task


class TaskListViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('tasks')
        self.user = AutoFixture(User).create(1)[0]
        fixture = AutoFixture(Task, field_values = {
            'owner': self.user
        })

        self.tasks = fixture.create(10)

    def test_task_list_lists_all_tasks(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(len(self.tasks), len(response.context['tasks']))

    def test_task_list_displays_users_tasks_only(self):
        other_user = AutoFixture(User).create(1)[0]
        AutoFixture(Task, field_values = {
            'owner': other_user
        }).create(1)

        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(len(self.tasks), len(response.context['tasks']))


class NewTaskViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('task-add')
        self.user = AutoFixture(User).create(1)[0]

    def test_create_task_always_forces_user(self):
        other_user = AutoFixture(User).create(1)[0]
        self.client.force_login(self.user)

        self.client.post(self.url, {
            'owner': other_user.id,
            'title': 'my task'
        }, follow = True)

        self.assertIsNotNone(Task.objects.first())
        self.assertEqual(Task.objects.first().owner, self.user)


class TaskViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = AutoFixture(User).create(1)[0]
        self.task = AutoFixture(Task, field_values = {
            'owner': self.user
        }).create(1)[0]
        self.url = reverse('task-edit', args = [self.task.id])

    def test_task_view_shows_update_form(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed('task.html')
        self.assertEqual(TaskForm, response.context['form'].__class__)
        self.assertTrue(response.context['update'])


class ToggleCompleteViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = AutoFixture(User).create(1)[0]
        self.client.force_login(self.user)

    def test_toggle_complete_toggles_complete(self):
        task = AutoFixture(Task, field_values = {
            'owner': self.user,
            'complete_time': None
        }).create(1)[0]

        url = reverse('task-toggle', args = [task.id])

        self.assertFalse(Task.objects.get(pk = task.id).is_complete)

        self.client.post(url)

        self.assertTrue(Task.objects.get(pk = task.id).is_complete)

    def test_toggle_incomplete_toggles_complete(self):
        task = AutoFixture(Task, field_values = {
            'owner': self.user,
            'complete_time': timezone.now() - timezone.timedelta(days = 1)
        }).create(1)[0]

        url = reverse('task-toggle', args = [task.id])

        self.assertTrue(Task.objects.get(pk = task.id).is_complete)

        self.client.post(url)

        self.assertFalse(Task.objects.get(pk = task.id).is_complete)

    def test_toggle_complete_returns_404(self):
        url = reverse('task-toggle', args = [12345])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        
