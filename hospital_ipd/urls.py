from django.urls import path
from . import views


app_name = 'ipd'
urlpatterns = [
    path('ipd/register/', views.register_page, name='register'),
]