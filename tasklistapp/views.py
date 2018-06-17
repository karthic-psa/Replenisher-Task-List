# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

from models import Task, TaskList
from task_form import AETaskForm


def staff_only(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# @login_required
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


# @login_required
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

    # if request.method == "POST":
    #     if "add_task" in request.POST:
    #         title = request.POST["title"]
    #         note = request.POST["note"]
    #         date_due = request.POST["date_due"]
    #         priority = request.POST["priority"]
    #         nTask = Task(title=title, note=note, date_due=date_due, priority=priority)
    #         nTask.save()
    #         return redirect("/")
    #
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

    if request.POST.get('toggle_done'):
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