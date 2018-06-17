
from django import forms
from django.contrib.auth.models import Group
from django.forms import ModelForm
from models import Task, TaskList


class TaskListForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(TaskListForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(user=user)
        self.fields['group'].widget.attrs = {
            'id': 'id_group', 'class': "custom-select mb-3", 'name': 'group'}

    class Meta:
        model = TaskList
        exclude = ['created_date', 'slug', ]


class AETaskForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(AETaskForm, self).__init__(*args, **kwargs)
        list_of_task = kwargs.get('initial').get('list_of_task')
        members = list_of_task.group.user_set.all()
        self.fields['user_assigned_to'].queryset = members
        self.fields['user_assigned_to'].label_from_instance = lambda obj: "%s (%s)" % (obj.get_full_name(), obj.username)
        self.fields['user_assigned_to'].widget.attrs = {
            'id': 'id_user_assigned_to', 'class': "custom-select mb-3", 'name': 'user_assigned_to'}
        self.fields['list_of_task'].value = kwargs['initial']['list_of_task'].id

    date_due = forms.DateField(
            widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    title = forms.CharField(
        widget=forms.widgets.TextInput())

    note = forms.CharField(
        widget=forms.Textarea(), required=False)

    class Meta:
        model = Task
        exclude = []
