# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils import timezone


class TaskList(models.Model):
    name = models.CharField(max_length=60)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    slug = models.SlugField(default='', )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Task Lists"
        unique_together = ("group", "slug")

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=140)
    list_of_task = models.ForeignKey(TaskList, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(default=timezone.now, blank=True, null=True)
    date_due = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(blank=True, null=True)
    priority = models.PositiveIntegerField()
    user_created = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_created_by', on_delete=models.CASCADE)
    user_assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                         related_name='task_assigned_to', on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["priority"]

    def overdue_status(self):
        if self.date_due and datetime.date.today() > self.date_due:
            return True

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'task_id': self.id, })

    def save(self, **kwargs):
        if self.completed:
            self.completed_date = datetime.datetime.now()
        super(Task, self).save()

    def __str__(self):
        return self.title


