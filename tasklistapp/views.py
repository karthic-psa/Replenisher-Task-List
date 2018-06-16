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