from django.urls import path
from . import (
    views, 
    doctor_appointment, 
    lab_appointment, 
    imaging_appointment
)


app_name = 'website'
urlpatterns = [
    
    # Real
    path('', views.home_page, name='home'),

    # electronic services - Doctors
    path('electronic/appointment/', doctor_appointment.eoa_home_page, name='el-oa-home'),
    path('electronic/appointment/categories/', doctor_appointment.eoa_categories_page, name='el-oa-categories'),
    path('electronic/appointment/doctors/', doctor_appointment.eoa_doctors_page, name='el-oad-doctors'),
    path('electronic/appointment/doctors/<doctorID>/phone/', doctor_appointment.eoa_phone_page, name='el-oad-phone'),
    path('electronic/appointment/doctors/enter-sms-code/<doctorID>/<uidb64>/<token>', doctor_appointment.eoa_entercode_page, name='el-oad-entercode'),
    path('electronic/appointment/doctors/<doctorID>/<uidb64>/<token>/calendar/', doctor_appointment.eoa_calendar_page, name='el-oad-calendar'),
    path('electronic/appointment/doctors/<doctorID>/<appointmentID>/<uidb64>/<token>/info/', doctor_appointment.eoa_info_page, name='el-oad-info'),
    path('electronic/appointment/doctors/<patientTurnId>/<uidb64>/<token>/show-details/', doctor_appointment.eoa_showdetails_page, name='el-oad-showdetails'),
    path('electronic/appointment/doctors/<patientTurnId>/<uidb64>/<token>/trust/', doctor_appointment.eoa_trust_page, name='el-oad-trust'),
    path('electronic/appointment/doctors/<patientTurnId>/<uidb64>/<token>/end/', doctor_appointment.eoa_end_page, name='el-oad-end'),

    # electronic services - lab
    path('electronic/appointment/lab/', lab_appointment.eoa_lab_page, name='el-oal-lab'),
    path('electronic/appointment/lab/list/', lab_appointment.eoa_lablist_page, name='el-oal-lablist'),
    path('electronic/appointment/lab/<doctorID>/phone/', doctor_appointment.eoa_phone_page, name='el-oal-phone'),

    # electronic services - imaging
    path('electronic/appointment/imaging/', imaging_appointment.eoa_imaging_page, name='el-oai-imaging'),

]