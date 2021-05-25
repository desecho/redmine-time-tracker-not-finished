# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth import logout
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseBadRequest

from .mixins import FormView, AjaxView
from ..forms import PreferencesForm
from ..models import Project


class PreferencesView(FormView):
    template_name = 'user/preferences.html'
    form_class = PreferencesForm

    def get_success_url(self):
        return reverse('preferences')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/login/')


class ImportProjectsView(AjaxView):
    """Import all projects from Redmine on which the user worked during the last n months."""
    def post(self, request):
        date_from = (datetime.date.today() -
                          datetime.timedelta(settings.PROJECT_IMPORT_NUMBER_OF_MONTHS * 365 / 12))
        user = request.user
        entries = user.redmine.time_entry.filter(user_id=user.redmine_user_id,
                                                         date_from=date_from).values()
        projects = {(entry['project']['id'], entry['project']['name']) for entry in entries}
        for project_id, project_name in projects:
            if not user.projects.filter(project_id=project_id).exists():
                Project.objects.create(user=user, name=project_name, project_id=project_id, project_type='redmine')
        return self.success()


class ToggleProjectView(AjaxView):
    """Hide or unhide a project."""
    def post(self, request):
        if 'id' not in request.POST:
            return HttpResponseBadRequest()
        project = get_object_or_404(Project, user=request.user, pk=request.POST['id'])
        project.is_hidden = not project.is_hidden
        project.save()
        return self.render_json_response({'status': 'success', 'is_hidden': project.is_hidden})
