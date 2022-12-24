from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from hospital_doctor.models import DoctorModel
from .decorators import online_doctor_required
from .mixins import DoctorRequired


# url: /panel/doctor/vacation/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_doctor_required
def doctor_vacation_page(request):
    return render(request, 'panel/online-appointment/tips.html')

