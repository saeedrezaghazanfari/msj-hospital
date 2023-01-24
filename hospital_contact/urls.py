from django.urls import path
from . import views


app_name = 'contact'
urlpatterns = [
    path('contact/careers/', views.careers_page, name='careers'),
    path('contact/careers/info/<careerCode>/', views.careers_info_page, name='careers-info'),
]