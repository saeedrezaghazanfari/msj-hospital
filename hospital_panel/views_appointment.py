from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from .decorators import online_appointment_required
from .mixins import OnlineAppointmentUserRequired
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from hospital_units.models import LimitTurnTimeModel


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


# url: /api/v1/limit-time/management/
class OnlineAppointmentManager(OnlineAppointmentUserRequired, APIView):

    def get(self, request):
        return Response({'status': 200})

    def delete(self, request):
        return Response({'status': 201})


