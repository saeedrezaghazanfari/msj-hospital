from django.urls import path
from . import (
    views,
    appointment_views,
)


app_name = 'website'
urlpatterns = [
    
    # Real
    path('', views.home_page, name='home'),
    path('read/notification/<notificationID>/', views.read_notification, name='read-notif'),

    # electronic services: online appointment
    path('electronic/appointment/turn/', appointment_views.eoa_followturn_page, name='oa-followupturn'),
    path('electronic/appointment/result/', appointment_views.eoa_followresult_page, name='oa-followupresult'),
    
    path('electronic/appointment/', appointment_views.eoa_home_page, name='oa-home'),
    path('electronic/appointment/categories/', appointment_views.eoa_categories_page, name='oa-categories'),
    path('electronic/appointment/<unitSlug>/router/', appointment_views.eoa_router_page, name='oa-router'),

    path('electronic/appointment/e-prescription/<unitSlug>/phone/', appointment_views.eoa_phone_epresc_page, name='oa-phone-pres'),
    path('electronic/appointment/e-prescription/<unitSlug>/enter-sms-code/<uidb64>/<token>/', appointment_views.eoa_entercode_pres_page, name='oa-entercode-pres'),
    path('electronic/appointment/e-prescription/<unitSlug>/<uidb64>/<token>/form/', appointment_views.eoa_electronic_pres_page, name='oa-electropres'),
    path('electronic/appointment/e-prescription/<unitSlug>/<uidb64>/<token>/show-details/', appointment_views.eoa_showdetails_pres_page, name='oa-showdetailspres'),
    
    path('electronic/appointment/<unitSlug>/', appointment_views.eoa_unit_page, name='oa-unit'),
    path('electronic/appointment/<unitSlug>/<doctorID>/phone/', appointment_views.eoa_phone_page, name='oa-phone'),
    path('electronic/appointment/<unitSlug>/enter-sms-code/<doctorID>/<uidb64>/<token>/', appointment_views.eoa_entercode_page, name='oa-entercode'),
    path('electronic/appointment/<unitSlug>/<doctorID>/<uidb64>/<token>/calendar/', appointment_views.eoa_calendar_page, name='oa-calendar'),
    path('electronic/appointment/<unitSlug>/<doctorID>/<appointmentID>/<uidb64>/<token>/info/', appointment_views.eoa_info_page, name='oa-info'),
    path('electronic/appointment/<unitSlug>/<patientTurnId>/<uidb64>/<token>/show-details/', appointment_views.eoa_showdetails_page, name='oa-showdetails'),
    path('electronic/appointment/<unitSlug>/<patientTurnId>/<uidb64>/<token>/trust/', appointment_views.eoa_trust_page, name='oa-trust'),
    path('electronic/appointment/<unitSlug>/<patientTurnId>/<uidb64>/<token>/end/', appointment_views.eoa_end_page, name='oa-end'),

]