from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from hospital_auth.models import User
from .forms import EditInfoForm


# url: /panel
class HomePage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        return context


# url: /panel/online-appointment
class OnlineAppointmentPage(generic.TemplateView):
    template_name = 'panel/online-appointment.html'


# url: /panel/edit-info
class EditInfoPage(generic.UpdateView):
    model = User
    form_class = EditInfoForm
    template_name = 'panel/edit-info.html'

    def get_success_url(self):
        return reverse_lazy('panel:home')


