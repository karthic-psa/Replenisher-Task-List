import pytest
from django.contrib.auth.models import Group, User
from tasklistapp.models import Task, TaskList


@pytest.fixture
def setup_model(django_user_model):

    group1 = Group.objects.create(name="TGT_One")
    user1 = django_user_model.objects.create_user(username="user1", password="asdf1234", email="user1@example.com")
    user1.groups.add(group1)
    tasklist1 = TaskList.objects.create(group=group1, name="ListOne", slug="listone")
    Task.objects.create(user_created=user1, title="Task 1", list_of_task=tasklist1, priority=3)
    Task.objects.create(user_created=user1, title="Task 2", list_of_task=tasklist1, priority=1, completed=True)
    Task.objects.create(user_created=user1, title="Task 3", list_of_task=tasklist1, priority=2)
    Task.objects.create(user_created=user1, title="Task 4", list_of_task=tasklist1, priority=4)
    Task.objects.create(user_created=user1, title="Task 5", list_of_task=tasklist1, priority=5, completed=True)

    group2 = Group.objects.create(name="TGT_Two")
    user2 = django_user_model.objects.create_user(username="user2", password="asdf1234", email="user2@example.com")
    user2.groups.add(group2)
    tasklist2 = TaskList.objects.create(group=group2, name="ListTwo", slug="listtwo")
    Task.objects.create(user_created=user2, title="Task 1", list_of_task=tasklist2, priority=1)
    Task.objects.create(user_created=user2, title="Task 2", list_of_task=tasklist2, priority=2, completed=True)
    Task.objects.create(user_created=user2, title="Task 3", list_of_task=tasklist2, priority=3)
    Task.objects.create(user_created=user2, title="Task 4", list_of_task=tasklist2, priority=4, completed=True)
    Task.objects.create(user_created=user2, title="Task 5", list_of_task=tasklist2, priority=5)
