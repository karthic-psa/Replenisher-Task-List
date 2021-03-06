# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from rest_framework.viewsets import ModelViewSet


from models import Task, TaskList
from task_form import AETaskForm, TaskListForm
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from serializers import TaskListViewSet, TaskViewSet, GroupSerializer, UserSerializer


class TaskListViewSet(ModelViewSet):
    queryset = TaskList.objects.all()
    serializer_class = TaskListViewSet


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all().order_by('priority')
    serializer_class = TaskViewSet


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def staff_only(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


@login_required
def task_lists(request):
    tdate = datetime.datetime.now()

    if request.user.groups.all().count() == 0:
        messages.warning(request, "You do not yet belong to any groups. Ask your administrator to add you to one.")

    if request.user.is_superuser:
        lists = TaskList.objects.all().order_by('group', 'name')
    else:
        lists = TaskList.objects.filter(group__in=request.user.groups.all()).order_by('group', 'name')

    cnt_list = lists.count()

    if request.user.is_superuser:
        cnt_task = Task.objects.filter(completed=0).count()
    else:
        cnt_task = Task.objects.filter(completed=0).filter(list_of_task__group__in=request.user.groups.all()).count()

    context = {
        "lists": lists,
        "tdate": tdate,
        "cnt_task": cnt_task,
        "cnt_list": cnt_list,
    }
    return render(request, 'index.html', context)


@login_required
def tasks_view(request, list_id=None, list_slug=None, view_completed=False):
    list_of_task = None
    form = None
    if list_slug == "personal":
        tasks = Task.objects.filter(user_assigned_to=request.user)
    else:
        list_of_task = get_object_or_404(TaskList, id=list_id)
        if list_of_task.group not in request.user.groups.all() and not request.user.is_staff:
            raise PermissionDenied
        tasks = Task.objects.filter(list_of_task=list_of_task.id)

    if view_completed:
        tasks = tasks.filter(completed=True)
    else:
        tasks = tasks.filter(completed=False)

    if request.POST.getlist('add_task'):
        form = AETaskForm(request.user, request.POST, initial={
            'user_assigned_to': request.user.id,
            'priority': 999,
            'list_of_task': list_of_task
        })

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.created_date = timezone.now()
            form.save()

            messages.success(request, "New task \"{t}\" has been added.".format(t=new_task.title))
            return redirect(request.path)
    else:
        if list_slug not in ["personal", "recent-add", "recent-complete", ]:
            form = AETaskForm(request.user, initial={
                'user_assigned_to': request.user.id,
                'priority': 999,
                'list_of_task': list_of_task,
            })
    context = {
        "list_id": list_id,
        "list_slug": list_slug,
        "list_of_task": list_of_task,
        "form": form,
        "tasks": tasks,
        "view_completed": view_completed,
    }

    return render(request, 'tasks_view.html', context)


@login_required
def task_toggle(request, task_id):

    task = get_object_or_404(Task, pk=task_id)

    if not (
        (task.user_created == request.user) or
        (task.user_assigned_to == request.user) or
        (task.list_of_task.group in request.user.groups.all())
    ):
        raise PermissionDenied

    listot = task.list_of_task
    task.completed = not task.completed
    task.save()

    messages.success(request, "Task status changed for '{}'".format(task.title))
    return redirect(reverse('tasks_view', kwargs={"list_id": listot.id, "list_slug": listot.slug}))


@login_required
def task_delete(request, task_id):

    task = get_object_or_404(Task, pk=task_id)

    if not (
        (task.user_created == request.user) or
        (task.user_assigned_to == request.user) or
        (task.list_of_task.group in request.user.groups.all())
    ):
        raise PermissionDenied

    tlist = task.list_of_task
    task.delete()

    messages.success(request, "Task '{}' has been deleted".format(task.title))
    return redirect(reverse('tasks_view', kwargs={"list_id": tlist.id, "list_slug": tlist.slug}))


@login_required
def task_detail(request, task_id):

    task = get_object_or_404(Task, pk=task_id)
    if task.list_of_task.group not in request.user.groups.all() and not request.user.is_staff:
        raise PermissionDenied

    if request.POST.get('add_task'):
        form = AETaskForm(request.user, request.POST, instance=task, initial={'list_of_task': task.list_of_task})

        if form.is_valid():
            form.save()
            messages.success(request, "The task has been edited.")
            return redirect('tasks_view', list_id=task.list_of_task.id, list_slug=task.list_of_task.slug)
    else:
        form = AETaskForm(request.user, instance=task, initial={'list_of_task': task.list_of_task})

    if request.POST.get('task_toggle'):
        results_changed = task_toggle([task.id, ])
        for res in results_changed:
            messages.success(request, res)

        return redirect('task_detail', task_id=task.id,)

    if task.date_due:
        thedate = task.date_due
    else:
        thedate = datetime.datetime.now()

    context = {
        "task": task,
        "form": form,
        "thedate": thedate,
    }

    return render(request, 'detail_of_task.html', context)


@staff_only
@login_required
def add_list(request):

    if request.POST:
        form = TaskListForm(request.user, request.POST)
        if form.is_valid():
            try:
                newlist = form.save(commit=False)
                newlist.slug = slugify(newlist.name)
                newlist.save()
                messages.success(request, "A new list has been added.")
                return redirect('task_lists')

            except IntegrityError:
                messages.warning(
                    request,
                    "There was a problem saving the new list. "
                    "Most likely a list with the same name in the same group already exists.")
    else:
        if request.user.groups.all().count() == 1:
            form = TaskListForm(request.user, initial={"group": request.user.groups.all()[0]})
        else:
            form = TaskListForm(request.user)

    context = {
        "form": form,
    }

    return render(request, 'new_list_add.html', context)


@staff_only
@login_required
def delete_list(request, list_id, list_slug):
    list_of_task = get_object_or_404(TaskList, slug=list_slug)

    if list_of_task.group not in request.user.groups.all() and not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        TaskList.objects.get(id=list_of_task.id).delete()
        messages.success(request, "{list_name} - list has been deleted.".format(list_name=list_of_task.name))
        return redirect('task_lists')
    else:
        task_count_done = Task.objects.filter(list_of_task=list_of_task.id, completed=True).count()
        task_count_undone = Task.objects.filter(list_of_task=list_of_task.id, completed=False).count()
        task_count_total = Task.objects.filter(list_of_task=list_of_task.id).count()

    context = {
        "list_of_task": list_of_task,
        "task_count_done": task_count_done,
        "task_count_undone": task_count_undone,
        "task_count_total": task_count_total,
    }
    return render(request, 'delete_list.html', context)
