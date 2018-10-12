from unittest import TestCase
from tasks.models import Task
from django.utils import timezone
from django.test import TransactionTestCase
import time


class TaskModelTestCase(TestCase):

    def test_complete_model_is_complete(self):
        target = Task()
        target.complete_time = timezone.now() - timezone.timedelta(days = 1)

        self.assertTrue(target.is_complete)

    def test_incomplete_model_is_incomplete(self):
        target = Task()
        target.complete_time = None

        self.assertFalse(target.is_complete)

    def test_future_complete_model_is_incomplete(self):
        target = Task()
        target.complete_time = timezone.now() + timezone.timedelta(days = 1)

        self.assertFalse(target.is_complete)

    def test_due_soon_model_is_due_soon(self):
        target = Task()
        target.due_date = timezone.now() + timezone.timedelta(days = 1)

        self.assertTrue(target.due_soon)

    def test_not_due_soon_model_is_not_due_soon(self):
        target = Task()
        target.due_date = timezone.now() + timezone.timedelta(days = 3)

        self.assertFalse(target.due_soon)

    def test_no_due_date_model_is_not_due_soon(self):
        target = Task()
        target.due_date = None

        self.assertFalse(target.due_soon)

    def test_mark_complete_marks_complete(self):
        target = Task()
        target.complete_time = None
        self.assertFalse(target.is_complete)

        target.mark_complete(commit = False)

        self.assertTrue(target.is_complete)

    def test_mark_incomplete_marks_incomplete(self):
        target = Task()
        target.complete_time = timezone.now()
        self.assertTrue(target.is_complete)

        target.mark_incomplete(commit = False)

        self.assertFalse(target.is_complete)


class TaskModelTransactionTestCase(TransactionTestCase):
    fixtures = ['tasks/fixtures/unit-tests.json']

    def test_fixtures_load(self):
        self.assertTrue(Task.objects.count() > 0)

    def test_mark_incomplete_persists(self):
        Task.objects.update(
            complete_time = timezone.now() + timezone.timedelta(days = 1)
        )

        target = Task.objects.first()
        target.mark_incomplete()
        self.assertFalse(Task.objects.get(pk = target.pk).is_complete)

    def test_mark_complete_persists(self):
        Task.objects.update(
            complete_time = None
        )

        target = Task.objects.first()
        target.mark_complete()
        self.assertTrue(Task.objects.get(pk = target.pk).is_complete)

    def test_time_impacts_due_soon(self):
        target = Task.objects.first()
        target.due_date = timezone.now() + timezone.timedelta(days = 2, seconds = 0.01)
        target.save()

        self.assertFalse(target.due_soon)
        time.sleep(0.1)
        self.assertTrue(target.due_soon)
