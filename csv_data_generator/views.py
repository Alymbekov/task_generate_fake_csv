from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

User = get_user_model()


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'


class NewSchemaView(generic.View):
    template_name = 'newschema.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        result = request.POST
        print(result)
        return render(request, self.template_name, {})
