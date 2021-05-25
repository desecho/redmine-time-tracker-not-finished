import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from redminelib.exceptions import AuthError, ResourceNotFoundError

from .redmine import redmine_api
from .models import Task, Project


class BootstrapForm(forms.Form):
    def _add_bootstrap_form_styles(self):
        for field_name in self.fields:
            field = self.fields[field_name]
            if not isinstance(field, forms.BooleanField) and not isinstance(field, forms.FileField):
                self.fields[field_name].widget.attrs['class'] = 'form-control'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_bootstrap_form_styles()


class TaskForm(BootstrapForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redmine = user.redmine
        self.fields['task_id'].widget.attrs.update({'autofocus': '', 'placeholder': _('Task id')})

    task_id = forms.CharField(required=True)

    def clean_task_id(self):
        task_id = self.cleaned_data['task_id']
        r = re.search(r'(\d+)', task_id)
        if r is None:
            raise forms.ValidationError(_('Invalid task id'))
        task_id = int(r.groups()[0])
        try:
            issue = self.redmine.issue.get(task_id)
        except ResourceNotFoundError:
            raise forms.ValidationError(_('Task not found'))
        if not hasattr(issue, 'story_points'):
            raise forms.ValidationError(_('The story has no estimate'))
        return issue

    def save(self):
        pass
        # TODO
        # api_key = self.cleaned_data['task_id']
        # if self.user.redmine_api_key != api_key:
        #     self.user.redmine_api_key = api_key
        #     self.user.save()


class PreferencesForm(BootstrapForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['initial'] = {'api_key': user.redmine_api_key}
        super().__init__(*args, **kwargs)
        self.fields['api_key'].widget.attrs.update({'autofocus': '', 'placeholder': _('API key')})

    api_key = forms.CharField(required=False, label=_('API key'))

    def clean_api_key(self):
        api_key = self.cleaned_data['api_key']
        if self.user.redmine_api_key != api_key:
            if api_key:
                redmine = redmine_api(api_key)
                try:
                    self.redmine_user = redmine.auth()
                except AuthError:
                    raise forms.ValidationError(_('Invalid authentication details'))
        return api_key

    def save(self):
        api_key = self.cleaned_data['api_key']
        if self.user.redmine_api_key != api_key:
            self.user.redmine_api_key = api_key
            if api_key:
                self.user.redmine_user_id = self.redmine_user.id
                self.user.first_name = self.redmine_user.firstname
                self.user.last_name = self.redmine_user.lastname
            self.user.save()
