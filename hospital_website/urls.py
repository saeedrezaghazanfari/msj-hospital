from django.urls import path
from . import views


app_name = 'website'
urlpatterns = [
    path('', views.home_page, name='home'),

    # electronic services
    path('electronic/appointment/', views.eoa_home_page, name='el-oa-home'),
    path('electronic/appointment/categories/', views.eoa_categories_page, name='el-oa-categories'),
    path('electronic/appointment/categories/doctors/', views.eoa_doctors_page, name='el-oa-doctors'),
    path('electronic/appointment/<int:medicalCode>/phone/', views.eoa_phone_page, name='el-oa-phone'),
    path('electronic/appointment/enter-sms-code/<medicalCode>/<uidb64>/<token>', views.eoa_entercode_page, name='el-oa-entercode'),
]