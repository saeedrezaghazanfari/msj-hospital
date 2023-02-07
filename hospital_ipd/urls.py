from django.urls import path
from . import views


app_name = 'ipd'
urlpatterns = [
    path('ipd/phone/', views.enter_phone_page, name='enter-phone'),
    path('ipd/enter-sms-code/<uidb64>/<token>/', views.enter_smscode_page, name='enter-smscode'),
    path('ipd/register/<uidb64>/<token>/', views.register_page, name='register'),

    path('ipd/login/', views.login_page, name='login'),
    path('ipd/info/<ipdId>/', views.info_page, name='info'),
]