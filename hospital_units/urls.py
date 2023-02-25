from django.urls import path
from . import views


app_name = 'units'
urlpatterns = [
    
    # electronic services: online appointment
    path('electronic/appointment/turn/', views.followturn_page, name='oa-followupturn'),
    path('electronic/appointment/result/', views.followresult_page, name='oa-followupresult'),
    
    path('electronic/appointment/', views.home_page, name='oa-home'),
    path('electronic/appointment/categories/', views.categories_page, name='oa-categories'),
    path('electronic/appointment/<unitSlug>/router/', views.router_page, name='oa-router'),

    path('electronic/appointment/e-prescription/<unitSlug>/phone/', views.phone_epresc_page, name='oa-phone-pres'),
    path('electronic/appointment/e-prescription/<unitSlug>/enter-sms-code/<uidb64>/<token>/', views.entercode_pres_page, name='oa-entercode-pres'),
    path('electronic/appointment/e-prescription/<unitSlug>/<uidb64>/<token>/form/', views.electronic_pres_page, name='oa-electropres'),
    path('electronic/appointment/e-prescription/<unitSlug>/<uidb64>/<token>/show-details/', views.showdetails_pres_page, name='oa-showdetailspres'),
    
    path('electronic/appointment/<unitSlug>/', views.unit_page, name='oa-unit'),
    path('electronic/appointment/<unitSlug>/<doctorID>/phone/', views.phone_page, name='oa-phone'),
    path('electronic/appointment/<unitSlug>/enter-sms-code/<doctorID>/<uidb64>/<token>/', views.entercode_page, name='oa-entercode'),
    path('electronic/appointment/<unitSlug>/<doctorID>/<uidb64>/<token>/<int:monthNum>/calendar/', views.calendar_page, name='oa-calendar'),
    path('electronic/appointment/<unitSlug>/<doctorID>/<appointmentID>/<uidb64>/<token>/info/', views.info_page, name='oa-info'),
    path('electronic/appointment/<unitSlug>/<patientTurnId>/<uidb64>/<token>/show-details/', views.showdetails_page, name='oa-showdetails'),
    path('electronic/appointment/<unitSlug>/<patientTurnId>/<uidb64>/<token>/trust/', views.trust_page, name='oa-trust'),
    path('electronic/appointment/<unitSlug>/<patientTurnId>/<uidb64>/<token>/end/', views.end_page, name='oa-end'),
]