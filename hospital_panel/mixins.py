from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class OnlineAppointmentUserRequired(AccessMixin):
    """Verify that the current user is online appointment access"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_appointment_manager:
            return redirect('/403')
        return super().dispatch(request, *args, **kwargs)


class DoctorRequired(AccessMixin):
    """Verify that the current user is online appointment access"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_doctor_manager:
            return redirect('/403')
        return super().dispatch(request, *args, **kwargs)
