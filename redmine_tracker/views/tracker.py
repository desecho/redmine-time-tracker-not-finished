# -*- coding: utf-8 -*-

from redminelib.exceptions import ResourceNotFoundError

from ..forms import TaskForm
from ..redmine import redmine_api
from .mixins import FormView


class HomeView(FormView):
    template_name = 'home.html'
    form_class = TaskForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO
        # tasks = self.request.session.get('tasks', [])
        # redmine = redmine_api(self.request.user.redmine_api_key)
        # context['tasks'] = []
        # for task_id in tasks:
        #     try:
        #         issue = redmine.issue.get(task_id)
        #         import ipdb; ipdb.set_trace()
        #     except ResourceNotFoundError:
        #         continue
        #     task = '#{} - {}'.format(task_id, issue.subject)
        #     context['tasks'].append(task)
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
