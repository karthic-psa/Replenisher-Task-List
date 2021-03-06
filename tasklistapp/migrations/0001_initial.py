# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-15 23:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('date_created', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('date_due', models.DateField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('date_completed', models.DateField(blank=True, null=True)),
                ('priority', models.PositiveIntegerField()),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='list_of_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tasklistapp.TaskList'),
        ),
        migrations.AddField(
            model_name='task',
            name='user_assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_assigned_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
