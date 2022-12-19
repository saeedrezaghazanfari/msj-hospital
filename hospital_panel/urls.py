from django.urls import path
from . import views, views_appointment


app_name = 'panel'
urlpatterns = [
    
    # Real pathes
    path('panel', views.home_page, name='home'),
    path('edit-info', views.edit_data, name='editdata'),

    # doctor management
    path('panel/doctor', views.doctor_page, name='doctor'),

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
    path('api/v1/limit-time/management/', views_appointment.OnlineAppointmentManager.as_view(), name='appointment-limittime-manager'),

]