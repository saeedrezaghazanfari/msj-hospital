from django.urls import path
from . import views


app_name = 'doctor'
urlpatterns = [
    path('doctor/list/', views.DoctorList.as_view(), name='doctors'),
    path('doctor/search/', views.doctor_search, name='search'),
    path('doctor/info/<uid>/', views.doctor_info, name='info'),
]