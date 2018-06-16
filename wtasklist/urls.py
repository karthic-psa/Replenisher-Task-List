"""wtasklist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from tasklistapp import views

app_name = 'tasklistapp'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tasks/', views.task_lists, name='task_lists'),
    url(r'^personal/',
        views.tasks_view,
        {'list_slug': 'personal'},
        name="personal"),

    url(r'^(?P<list_id>[0-9]+)/(?P<list_slug>\w+)/completed/',
        views.tasks_view,
        {'view_completed': True},
        name='tasks_view_completed'),

    url(r'^(?P<list_id>[0-9]+)/(?P<list_slug>\w+)/',
        views.tasks_view,
        name='tasks_view'),

    url(
        r'^task_toggle/(?P<task_id>[0-9]+)/',
        views.task_toggle,
        name='task_toggle_done'),
]
