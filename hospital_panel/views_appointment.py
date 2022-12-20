from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from hospital_units.models import LimitTurnTimeModel, AppointmentTipModel
from hospital_setting.models import InsuranceModel
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


# url: /panel/online-appointment/insurances/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_insurances_page(request):
    return render(request, 'panel/online-appointment/insurances.html')


# url: /api/v1/insurances/management/
class InsurancesManager(OnlineAppointmentUserRequired, APIView):

    def get(self, request):
        insurances = InsuranceModel.objects.all()
        
        return Response({
            'data': serializers.InsuranceSerializer(insurances, many=True).data,
            'status': 200
        })

    def post(self, request):
        
        serializer = serializers.InsuranceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        insurance = InsuranceModel.objects.create(
            title=request.data.get('title'),
            img=request.data.get('img')
        )

        return Response({
            'data': serializers.InsuranceSerializer(insurance).data,
            'msg': _('بیمه ی مورد نظر با موفقیت ذخیره شد.'),
            'status': 200
        })


# url: /panel/online-appointment/tips/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_tips_page(request):
    return render(request, 'panel/online-appointment/tips.html')


# url: /api/v1/tips/management/
class TipsManager(OnlineAppointmentUserRequired, APIView):

    def get(self, request):
        tips = AppointmentTipModel.objects.all()
        
        return Response({
            'data': serializers.AppointmentTipSerializer(tips, many=True).data,
            'status': 200
        })

    def post(self, request):
        
        serializer = serializers.AppointmentTipSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tips = AppointmentTipModel.objects.create(
            title=request.data.get('title'),
            tips=request.data.get('tips')
        )

        return Response({
            'data': serializers.AppointmentTipSerializer(tips).data,
            'msg': _('نکات مورد نظر با موفقیت ذخیره شد.'),
            'status': 200
        })