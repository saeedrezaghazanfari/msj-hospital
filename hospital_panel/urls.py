from django.urls import path
from . import views, views_appointment, views_doctor


app_name = 'panel'
urlpatterns = [
    
    # Real pathes
    path('panel', views.home_page, name='home'),
    path('panel/edit-info', views.edit_data, name='editdata'),


    # doctor management
    path('panel/doctor', views.doctor_page, name='doctor'),
    path('panel/doctor/vacation/', views_doctor.doctor_vacation_page, name='doctor-vacation'),
    path('panel/doctor/work/', views_doctor.doctor_work_page, name='doctor-work'),
    path('panel/doctor/insurances/', views_doctor.doctor_insurances_page, name='doctor-insurances'),


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
    path('panel/online-appointment/tips/sms/', views_appointment.oa_smstips_page, name='appointment-smstips'),
    path('panel/online-appointment/skill/', views_appointment.oa_skilltitle_page, name='appointment-skill'),
    path('panel/online-appointment/degree/', views_appointment.oa_degree_page, name='appointment-degree'),
    path('panel/online-appointment/unit/', views_appointment.oa_unit_page, name='appointment-unit'),
    path('panel/online-appointment/subunit/', views_appointment.oa_subunit_page, name='appointment-subunit'),
    path('panel/online-appointment/doctor/list/', views_appointment.oa_doctorlist_page, name='appointment-doctorlist'),
    path('panel/online-appointment/doctor/create/', views_appointment.oa_doctorcreate_page, name='appointment-doctorcreate'),
    path('panel/online-appointment/doctor/<doctorId>/times/', views_appointment.oa_doctorlist_time_page, name='appointment-doctorlist-times'),
    path('panel/online-appointment/price/', views_appointment.oa_price_page, name='appointment-price'),
    path('panel/online-appointment/time/', views_appointment.oa_time_page, name='appointment-time'),
    path('panel/online-appointment/time/<appointmentID>/edit/', views_appointment.oa_time_edit_page, name='appointment-timeedit'),
    path('panel/online-appointment/time/create/', views_appointment.oa_time_create0_page, name='appointment-timep0'),
    path('panel/online-appointment/time/create/<unitID>/', views_appointment.oa_time_create1_page, name='appointment-timep1'),
    path('panel/online-appointment/time/create/<unitID>/<doctorId>/', views_appointment.oa_time_create2_page, name='appointment-timep2'),
    path('panel/online-appointment/patient/', views_appointment.oa_patient_page, name='appointment-patient'),
    path('panel/online-appointment/e-turn/', views_appointment.oa_eturn_list_page, name='appointment-eturnlist'),
    path('panel/online-appointment/e-turn/<eturnID>/', views_appointment.oa_eturn_check_page, name='appointment-eturncheck'),
]