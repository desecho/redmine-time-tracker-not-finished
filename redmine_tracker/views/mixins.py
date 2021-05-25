from braces.views import JsonRequestResponseMixin, LoginRequiredMixin
from django.views.generic import TemplateView as TemplateViewOriginal
from django.views.generic import View
from django.views.generic.edit import FormView as FormViewOriginal


class AjaxView(LoginRequiredMixin, JsonRequestResponseMixin, View):
    def success(self):
        return self.render_json_response({'status': 'success'})


class TemplateView(LoginRequiredMixin, TemplateViewOriginal):
    pass


class FormView(LoginRequiredMixin, FormViewOriginal):
    pass
