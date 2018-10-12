from unittest import TestCase
from tasks.mixins import SuccessTaskListMixin
from django.urls import reverse


class SuccessTaskListMixinTestCase(TestCase):

    def setUp(self):
        # Implement mixins
        class MyClass(SuccessTaskListMixin):
            pass

        self.target = MyClass()

    def test_get_success_url_returns_correct_url(self):
        target_url = reverse('tasks')

        result = self.target.get_success_url()

        self.assertEqual(target_url, result)
