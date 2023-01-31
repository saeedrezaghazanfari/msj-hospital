from django.urls import path
from . import views


app_name = 'doctor'
urlpatterns = [
    path('doctor/list/', views.DoctorList.as_view(), name='doctors'),
    path('doctor/info/<medicalId>/', views.doctor_info, name='info'),
]