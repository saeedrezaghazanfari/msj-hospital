from django.urls import path
from . import views


app_name = 'panel'
urlpatterns = [
    
    # Real pathes
    path('panel', views.HomePage.as_view(), name='home'),
    path('panel/online-appointment', views.OnlineAppointmentPage.as_view(), name='online-appointment'),
    path('panel/activate-account', views.ActivateAccountPage.as_view(), name='activate-account'),
    path('panel/edit-info', views.EditInfoPage.as_view(), name='edit-info'),
    path('panel/reset-password', views.ResetPassWordPage.as_view(), name='reset-password'),

    # Doctor pathes
    # path('panel/doctor', views.DoctorHomePage.as_view(), name='doctor-home'),

]