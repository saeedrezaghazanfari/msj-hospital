from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class PanelHomePage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/home.html'

    def get_context_data(self, **kwargs):
        context = super(PanelHomePage, self).get_context_data(**kwargs)
        return context
