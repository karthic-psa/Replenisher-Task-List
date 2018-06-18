from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from tasklistapp.models import  TaskList, Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class TaskListViewSet(ModelSerializer):

    class Meta:
        model = TaskList
        fields = '__all__'


class TaskViewSet(ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
