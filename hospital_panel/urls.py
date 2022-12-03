from django.urls import path
from . import views


app_name = 'panel'
urlpatterns = [
    path('panel', views.PanelHomePage.as_view(), name='home'),
]