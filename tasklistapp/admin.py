# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Task, TaskList


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'list_of_task', 'completed', 'priority', 'date_due')
    list_filter = ('list_of_task',)
    ordering = ('priority',)


admin.site.register(TaskList)
admin.site.register(Task, TaskAdmin)