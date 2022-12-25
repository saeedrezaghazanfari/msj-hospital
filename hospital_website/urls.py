from django.urls import path
from . import views, doctor_appointment


app_name = 'website'
urlpatterns = [
    
    # Real
    path('', views.home_page, name='home'),

    # electronic services - Doctors
    path('electronic/appointment/', doctor_appointment.eoa_home_page, name='el-oa-home'),
    path('electronic/appointment/categories/', doctor_appointment.eoa_categories_page, name='el-oa-categories'),
    path('electronic/appointment/categories/doctors/', doctor_appointment.eoa_doctors_page, name='el-oa-doctors'),
    path('electronic/appointment/<int:medicalCode>/phone/', doctor_appointment.eoa_phone_page, name='el-oa-phone'),
    path('electronic/appointment/enter-sms-code/<medicalCode>/<uidb64>/<token>', doctor_appointment.eoa_entercode_page, name='el-oa-entercode'),
    path('electronic/appointment/<medicalCode>/<uidb64>/<token>/calendar/', doctor_appointment.eoa_calendar_page, name='el-oa-calendar'),
    path('electronic/appointment/<medicalCode>/<appointmentID>/<uidb64>/<token>/info/', doctor_appointment.eoa_info_page, name='el-oa-info'),
    path('electronic/appointment/<patientTurnId>/<uidb64>/<token>/show-details/', doctor_appointment.eoa_showdetails_page, name='el-oa-showdetails'),
    path('electronic/appointment/<patientTurnId>/<uidb64>/<token>/trust/', doctor_appointment.eoa_trust_page, name='el-oa-trust'),
    path('electronic/appointment/<patientTurnId>/<uidb64>/<token>/end/', doctor_appointment.eoa_end_page, name='el-oa-end'),


]