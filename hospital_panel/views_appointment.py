from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from hospital_units.models import LimitTurnTimeModel
from .decorators import online_appointment_required
from .mixins import OnlineAppointmentUserRequired
from . import serializers


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

    def post(self, request):
        """ create a new limit time in db for user online appointment """
        
        serializer = serializers.LimitTurnTimeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if LimitTurnTimeModel.objects.exists():
            LimitTurnTimeModel.objects.all().delete()

        limit_time = LimitTurnTimeModel.objects.create(
            to_hour=request.data.get('to_hour'),
            how_days_hour=request.data.get('how_days_hour')
        )

        return Response({
            'data': serializers.LimitTurnTimeSerializer(limit_time).data,
            'msg': _('حد زمانی برای ثبت نوبت اینترنتی کاربران با موفقیت ذخیره شد.'),
            'status': 200
        })



