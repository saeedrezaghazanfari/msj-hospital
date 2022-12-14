from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from hospital_auth.models import User
# from .forms import EditInfoForm


# url: /panel
class HomePage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        return context




# url: /panel/doctor
class DoctorPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/doctor/home.html'


# url: /panel/blog
class BlogPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/blog/home.html'


# url: /panel/news
class NewsPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/news/home.html'


# url: /panel/notes
class NotesPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/notes/home.html'


# url: /panel/experiment
class ExperimentPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/experiment/home.html'


# url: /panel/online-appointment
class OnlineAppointmentPage(generic.TemplateView):
    template_name = 'panel/online-appointment/home.html'


















