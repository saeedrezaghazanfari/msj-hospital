from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from hospital_units.models import LimitTurnTimeModel
from .decorators import online_appointment_required


# url: /panel/online-appointment
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url='/403')
def online_appointment_page(request):
    return render(request, 'panel/online-appointment/home.html', {})


# url: /panel/online-appointment/limit-time/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_limit_time_page(request):
    
    limit_time = LimitTurnTimeModel.objects.last()
    return render(request, 'panel/online-appointment/limittime.html', {
        'limit_time': limit_time
    })


# url: /panel/online-appointment/insurances/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_insurances_page(request):
    return render(request, 'panel/online-appointment/insurances.html')


# url: /panel/online-appointment/tips/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_tips_page(request):
    return render(request, 'panel/online-appointment/tips.html')


# url: /panel/online-appointment/doctor/list/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_doctorlist_page(request):
    return render(request, 'panel/online-appointment/doctor-list.html')
