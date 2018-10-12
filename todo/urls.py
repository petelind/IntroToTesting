from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tasks import views as tasks_views
from .views import Home, register
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # Home
    url(r'^$', Home.as_view(), name = 'home'),

    # Authentication and registration
    url(r'^login/$', auth_views.login, name = 'login'),
    url(r'^logout/$', auth_views.logout, name = 'logout'),
    url(r'^register/$', register, name='register'),

    # Task management
    url(r'^tasks/$',
        login_required(tasks_views.TaskListView.as_view(), login_url = 'login'),
        name = 'tasks'),

    url(r'^task/$',
        login_required(tasks_views.NewTaskView.as_view()),
        name = 'task-add'),

    url(r'^task/(?P<task_id>\d+)/$',
        login_required(tasks_views.TaskView.as_view()),
        name = 'task-edit'),

    url(r'^delete/(?P<task_id>\d+)/$',
        login_required(tasks_views.DeleteTaskView.as_view()),
        name = 'task-delete'),

    url(r'^toggle/(?P<task_id>\d+)/$',
        login_required(tasks_views.toggle_complete_view),
        name = 'task-toggle'),

    # Django admin
    url(r'^admin/', admin.site.urls),
]
