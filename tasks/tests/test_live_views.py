from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from autofixture import AutoFixture
from django.contrib.auth.models import User
from tasks.models import Task


class TasksViewsStaticLiveServerTestCae(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(TasksViewsStaticLiveServerTestCae, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(TasksViewsStaticLiveServerTestCae, cls).tearDownClass()

    def setUp(self):
        self.username = 'myuser'
        self.password = 'valid_password1'
        self.user = User.objects.create_user(
            self.username, 'email@test.com', self.password
        )
        AutoFixture(Task, field_values = {
            'owner': self.user,
            'complete_time': None
        }).create(1)

    def login(self):
        self.selenium.get(self.live_server_url)
        username_input = self.selenium.find_element_by_name("username")
        password_input = self.selenium.find_element_by_name("password")

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)

        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

    def get_task_check_button(self):
        return self.selenium.find_element_by_css_selector('.task-complete span')

    def test_toggle(self):
        self.login()
        task_check_button = self.get_task_check_button()
        self.assertTrue('glyphicon-blue' in task_check_button.get_attribute('class'))

        task_check_button.click()

        task_check_button = self.get_task_check_button()
        self.assertTrue('glyphicon-red' in task_check_button.get_attribute('class'))
