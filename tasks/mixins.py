from django.shortcuts import get_object_or_404
from .models import Task


class SuccessTaskListMixin(object):
    """
    Uses lazy imported reverse to resolve success URL
    for views that redirect to task list view.
    Note: This is not absolutely necessary, as reversible
    name can be used in success_url attribute for most classes.
    """
    def get_success_url(self):
        from django.urls import reverse
        return reverse('tasks')


class TaskOwnedByUserMixin(object):
    """
    For methods that manipulate tasks via POST, a mixin that
    ensures the current logged in user owns the specified task.
    If not, return a 404 instead of a 403 to obfuscate the existence
    of that task.
    """
    def post(self, request, task_id = None, *args, **kwargs):
        if task_id:
            # Validate that user owns task or 404
            get_object_or_404(Task, pk = task_id, owner = request.user)

        return super(TaskOwnedByUserMixin, self).post(request, *args, **kwargs)
