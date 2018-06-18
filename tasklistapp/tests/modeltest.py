import pytest

from django.contrib.auth.models import Group

from tasklistapp.models import Task, TaskList


@pytest.fixture
def todo_setup(django_user_model):

    group1 = Group.objects.create(name="Task Group One")
    user1 = django_user_model.objects.create_user(username="user1", password="asdf1234", email="user1@example.com")
    user1.groups.add(group1)
    tlist1 = TaskList.objects.create(group=g1, name="TestList1", slug="zip")
    Task.objects.create(user_created=user1, title="Task 1", list_of_task=tlist1, priority=3)
    Task.objects.create(user_created=user1, title="Task 2", list_of_task=tlist1, priority=1, completed=True)
    Task.objects.create(user_created=user1, title="Task 3", list_of_task=tlist1, priority=2)
    Task.objects.create(user_created=user1, title="Task 4", list_of_task=tlist1, priority=4)
    Task.objects.create(user_created=user1, title="Task 5", list_of_task=tlist1, priority=5, completed=True)

    group2 = Group.objects.create(name="Task Group Two")
    user2 = django_user_model.objects.create_user(username="user2", password="asdf1234", email="user2@example.com")
    user2.groups.add(group2)
    tlist2 = TaskList.objects.create(group=g2, name="Zap", slug="TestList2")
    Task.objects.create(user_created=user2, title="Task 1", list_of_task=tlist2, priority=1)
    Task.objects.create(user_created=user2, title="Task 2", list_of_task=tlist2, priority=2, completed=True)
    Task.objects.create(user_created=user2, title="Task 3", list_of_task=tlist2, priority=3)
    Task.objects.create(user_created=user2, title="Task 4", list_of_task=tlist2, priority=4, completed=True)
    Task.objects.create(user_created=user2, title="Task 5", list_of_task=tlist2, priority=5)