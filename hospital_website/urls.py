from django.urls import path
from . import views


app_name = 'website'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('about-us/', views.aboutus_page, name='aboutus'),
    # path('history/', views.history_page, name='history'),
    path('search/', views.search_page, name='search'),
    path('newsletter/register/', views.newsletter_page, name='email-newsletter'),
]