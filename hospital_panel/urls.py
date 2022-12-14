from django.urls import path
from . import views


app_name = 'panel'
urlpatterns = [
    
    # Real pathes
    path('panel', views.HomePage.as_view(), name='home'),

    # doctor management
    path('panel/doctor', views.DoctorPage.as_view(), name='doctor'),

    # blog management
    path('panel/blog', views.BlogPage.as_view(), name='blog'),

    # news management
    path('panel/news', views.NewsPage.as_view(), name='news'),

    # note management
    path('panel/notes', views.NotesPage.as_view(), name='notes'),

    # experiment management
    path('panel/experiment', views.ExperimentPage.as_view(), name='experiment'),

    # online appointment management
    path('panel/online-appointment', views.OnlineAppointmentPage.as_view(), name='appointment'),

]