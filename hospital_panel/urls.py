from django.urls import path
from . import views, views_appointment, views_doctor


app_name = 'panel'
urlpatterns = [
    
    # Real pathes
    path('panel', views.home_page, name='home'),
    path('edit-info', views.edit_data, name='editdata'),


    # doctor management
    path('panel/doctor', views.doctor_page, name='doctor'),
    path('panel/doctor/vacation/', views_doctor.doctor_vacation_page, name='doctor-vacation'),


    # blog management
    path('panel/blog', views.blog_page, name='blog'),


    # news management
    path('panel/news', views.news_page, name='news'),


    # note management
    path('panel/notes', views.notes_page, name='notes'),


    # experiment management
    path('panel/experiment', views.experiment_page, name='experiment'),


    # online appointment management
    path('panel/online-appointment', views_appointment.online_appointment_page, name='appointment'), 
    path('panel/online-appointment/limit-time/', views_appointment.oa_limit_time_page, name='appointment-limittime'),
    path('panel/online-appointment/insurances/', views_appointment.oa_insurances_page, name='appointment-insurances'),
    path('panel/online-appointment/tips/', views_appointment.oa_tips_page, name='appointment-tips'),
    path('panel/online-appointment/doctor/list/', views_appointment.oa_doctorlist_page, name='appointment-doctorlist'),
    path('panel/online-appointment/doctor/<int:medicalCode>/times/', views_appointment.oa_doctorlist_time_page, name='appointment-doctorlist-times'),
    path('panel/online-appointment/price/', views_appointment.oa_price_page, name='appointment-price'),
    path('panel/online-appointment/time/', views_appointment.oa_time_page, name='appointment-time'),
    path('panel/online-appointment/patient/', views_appointment.oa_patient_page, name='appointment-patient'),
]