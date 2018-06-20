import pytest

from django.contrib.auth.models import Group
from django.urls import reverse
from tasklistapp.models import Task, TaskList


@pytest.mark.django_db
def test_setup(setup_model):
    assert Task.objects.all().count() == 10


def test_tasks_list_index(setup_model, admin_client):
    url = reverse('task_lists')
    response = admin_client.get(url)
    assert response.status_code == 200


def test_my_tasks(setup_model, admin_client):
    url = reverse('personal')
    response = admin_client.get(url)
    assert response.status_code == 200


def test_tasks_completed(setup_model, admin_client):
    tlist = TaskList.objects.get(slug="listone")
    url = reverse('tasks_view_completed', kwargs={'list_id': tlist.id, 'list_slug': tlist.slug})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_tasks_view(setup_model, admin_client):
    tlist = TaskList.objects.get(slug="listone")
    url = reverse('tasks_view', kwargs={'list_id': tlist.id, 'list_slug': tlist.slug})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_delete_list(setup_model, admin_client):
    tlist = TaskList.objects.get(slug="listone")
    url = reverse('delete_list', kwargs={'list_id': tlist.id, 'list_slug': tlist.slug})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_add_list(setup_model, admin_client):
    url = reverse('add_list')
    response = admin_client.get(url)
    assert response.status_code == 200


def test_task_detail(setup_model, admin_client):
    task = Task.objects.first()
    url = reverse('task_detail', kwargs={'task_id': task.id})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_add_list_nonadmin(setup_model, client):
    url = reverse('add_list')
    client.login(username="you", password="password")
    response = client.get(url)
    assert response.status_code == 403


def test_del_list_nonadmin(setup_model, client):
    tlist = TaskList.objects.get(slug="listone")
    url = reverse('delete_list', kwargs={'list_id': tlist.id, 'list_slug': tlist.slug})
    client.login(username="you", password="password")
    response = client.get(url)
    assert response.status_code == 403


def test_list_personal(setup_model, client):
    """View a list in a group I belong to.
    """
    tlist = TaskList.objects.get(slug="listone")  # User u1 is in this group's list
    url = reverse('tasks_view', kwargs={'list_id': tlist.id, 'list_slug': tlist.slug})
    client.login(username="user1", password="asdf1234")
    response = client.get(url)
    assert response.status_code == 200


def test_list_not_personal(setup_model, client):
    """View a list in a group I don't belong to.
    """
    tlist = TaskList.objects.get(slug="listone")  # User u1 is in this group, user u2 is not.
    url = reverse('tasks_view', kwargs={'list_id': tlist.id, 'list_slug': tlist.slug})
    client.login(username="user2", password="asdf1234")
    response = client.get(url)
    assert response.status_code == 403


def test_task_personal(setup_model, client):
    # Users can always view their own tasks
    task = Task.objects.filter(user_created__username="user1").first()
    client.login(username="user1", password="asdf1234")
    url = reverse('task_detail', kwargs={'task_id': task.id})
    response = client.get(url)
    assert response.status_code == 200


def test_task_my_group(setup_model, client, django_user_model):
    # User can always view tasks that are NOT theirs IF the task is in a shared group.
    # u1 and u2 are in different groups in the fixture -
    # Put them in the same group.
    group1 = Group.objects.get(name="TGT_One")
    user2 = django_user_model.objects.get(username="user2")
    user2.groups.add(group1)

    # Now u2 should be able to view one of u1's tasks.
    task = Task.objects.filter(user_created__username="user1").first()
    url = reverse('task_detail', kwargs={'task_id': task.id})
    client.login(username="user2", password="asdf1234")
    response = client.get(url)
    assert response.status_code == 200


def test_task_not_in_my_group(setup_model, client):
    # User canNOT view a task that isn't theirs if the two users are not in a shared group.
    # For this we can use the fixture data as-is.
    task = Task.objects.filter(user_created__username="user1").first()
    url = reverse('task_detail', kwargs={'task_id': task.id})
    client.login(username="user2", password="asdf1234")
    response = client.get(url)
    assert response.status_code == 403
