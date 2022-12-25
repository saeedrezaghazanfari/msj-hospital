from django.urls import path
from . import views


app_name = 'website'
urlpatterns = [
    path('', views.home_page, name='home'),

    # electronic services
    path('electronic/appointment/', views.eoa_home_page, name='el-oa-home'),
    path('electronic/appointment/categories/', views.eoa_categories_page, name='el-oa-categories'),
    path('electronic/appointment/categories/doctors/', views.eoa_doctors_page, name='el-oa-doctors'),
    path('electronic/appointment/<int:medicalCode>/phone/', views.eoa_phone_page, name='el-oa-phone'),
    path('electronic/appointment/enter-sms-code/<medicalCode>/<uidb64>/<token>', views.eoa_entercode_page, name='el-oa-entercode'),
    path('electronic/appointment/<medicalCode>/<uidb64>/<token>/calendar/', views.eoa_calendar_page, name='el-oa-calendar'),
    path('electronic/appointment/<medicalCode>/<appointmentID>/<uidb64>/<token>/info/', views.eoa_info_page, name='el-oa-info'),
    path('electronic/appointment/<patientTurnId>/<uidb64>/<token>/show-details/', views.eoa_showdetails_page, name='el-oa-showdetails'),
    path('electronic/appointment/<patientTurnId>/<uidb64>/<token>/trust/', views.eoa_trust_page, name='el-oa-trust'),
    path('electronic/appointment/<patientTurnId>/<uidb64>/<token>/end/', views.eoa_end_page, name='el-oa-end'),
]