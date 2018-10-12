from behave import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from autofixture import AutoFixture
from django.contrib.auth.models import User
from tasks.models import Task

use_step_matcher("re")


@given("I'm registered user")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.selenium = WebDriver()
    context.selenium.implicitly_wait(10)

    context.username = 'myuser'
    context.password = 'valid_password1'
    context.user = User.objects.create_user(
        context.username, 'email@test.com', context.password
    )

    context.live_server_url = context.get_url()

@step("I have task pending")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    AutoFixture(Task, field_values={
        'owner': context.user,
        'complete_time': None
    }).create(1)


@when("I log in I see my tasks and toggle button is blue")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.selenium.get(context.live_server_url)
    username_input = context.selenium.find_element_by_name("username")
    password_input = context.selenium.find_element_by_name("password")

    username_input.send_keys(context.username)
    password_input.send_keys(context.password)

    context.selenium.find_element_by_css_selector('button[type="submit"]').click()
    context.task_check_button = context.selenium.find_element_by_css_selector('.task-complete span')

    assert ('glyphicon-blue' in context.task_check_button.get_attribute('class'))


@when('I click "complete" task toggle turns red')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

@when('I click "complete"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.task_check_button.click()


@then("task toggle turns red")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert ('glyphicon-red' in context.task_check_button.get_attribute('class'))