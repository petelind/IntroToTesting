from __future__ import unicode_literals

from django.utils import timezone

from django.db import models
from django.conf import settings


class TaskManger(models.Manager):
    def get_queryset(self):
        queryset = super(TaskManger, self).get_queryset()
        return queryset.order_by('complete_time', 'due_date')


class Task(models.Model):
    """
    Task

    The most important model for this application.
    Allows users to create and edit tasks that they
    need to complete. They can set names, descriptions,
    and due dates.
    """
    objects = TaskManger()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    title = models.CharField(max_length = 100, null = False)
    description = models.TextField(blank = True)
    due_date = models.DateField(blank = True, null = True)
    complete_time = models.DateTimeField(blank = True, null = True)

    @property
    def is_complete(self):
        """
        Checks if a task is complete.
        :return: True if task has been completed as indicated by a truthy
        value for complete_time. Otherwise, False.
        """
        return bool(
            self.complete_time and self.complete_time < timezone.now())

    @property
    def due_soon(self):
        """
        Checks if a task is due soon.
        :return: True if task is due within two days. Otherwise, False.
        """
        # explicit __add__ used due to failing type checking in some IDEs
        min_due = timezone.now().__add__(timezone.timedelta(days = 2))
        return bool(
            self.due_date and self.due_date < min_due)

    def mark_complete(self, commit = True):
        """
        Marks a task as complete by storing the current UTC time in complete_time
        """
        self.complete_time = timezone.now()
        if commit:
            self.save()

    def mark_incomplete(self, commit = True):
        """
        Marks a task as incomplete by storing None in complete_time
        """
        self.complete_time = None
        if commit:
            self.save()
