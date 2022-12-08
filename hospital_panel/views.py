from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


# url: /panel
class HomePage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        return context


# url: /panel/online-appointment
class OnlineAppointmentPage(generic.TemplateView):
    template_name = 'panel/online-appointment.html'


# url: /panel/activate-account
class ActivateAccountPage(generic.TemplateView):
    template_name = 'panel/activate-account.html'


# url: /panel/edit-info
class EditInfoPage(generic.TemplateView):
    template_name = 'panel/edit-info.html'


# url: /panel/reset-password
class ResetPassWordPage(generic.TemplateView):
    template_name = 'panel/reset-password.html'


