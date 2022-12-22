from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from hospital_units.models import LimitTurnTimeModel, AppointmentTipModel
from hospital_setting.models import InsuranceModel
from hospital_doctor.models import DoctorModel
from .mixins import OnlineAppointmentUserRequired
from . import serializers


# url: /api/v1/limit-time/
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


# url: /api/v1/online-appointment/insurances/
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


# url: /api/v1/online-appointment/tips/
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


# url: /api/v1/online-appointment/doctor/list/
class AppointmentDoctorManager(OnlineAppointmentUserRequired, APIView):

    def get(self, request):

        doctors = DoctorModel.objects.all()
        return Response({
            'data': serializers.DoctorSerializer(doctors, many=True).data,
            'status': 200
        })

    def post(self, request):

        code = request.data.get('code')
        
        if code and DoctorModel.objects.filter(medical_code=code).exists():
            
            doctor = DoctorModel.objects.get(medical_code=code)

            works = doctor.doctorworktimemodel_set.all()
            vacations = doctor.doctorvacationmodel_set.all()

            return Response({
                'works': serializers.DoctorWorkSerializer(works, many=True).data,
                'vacations': serializers.DoctorVacationSerializer(vacations, many=True).data,
                'status': 200
            })
        return Response({'status': 400})


    def patch(self, request):

        code = request.data.get('code')
        
        if code and DoctorModel.objects.filter(medical_code=code).exists():
            
            doctor = DoctorModel.objects.get(medical_code=code)
            doctor.doctorvacationmodel_set.filter(is_accepted=False).update(is_accepted=True)

            works = doctor.doctorworktimemodel_set.all()
            vacations = doctor.doctorvacationmodel_set.all()

            return Response({
                'works': serializers.DoctorWorkSerializer(works, many=True).data,
                'vacations': serializers.DoctorVacationSerializer(vacations, many=True).data,
                'status': 200
            })
        return Response({'status': 400})