from django.urls import path
from . import views


app_name = 'website'
urlpatterns = [

    # real
    path('', views.home_page, name='home'),
    path('search/', views.search_page, name='search'),
    path('newsletter/register/', views.newsletter_page, name='email-newsletter'),

    # about-us tab
    path('about-us/', views.aboutus_page, name='aboutus'),
    path('history/', views.history_page, name='history'),
    path('workshops/', views.workshops_page, name='workshops'),
    path('certificates/', views.certificates_page, name='certificates'),
    path('gallery/images/', views.gallery_imgs_page, name='gallery-imgs'),
    path('gallery/videos/', views.gallery_vids_page, name='gallery-vids'),
    path('policies/', views.policies_page, name='policies'),
    path('management/', views.management_page, name='management'),
    path('chart/', views.chart_page, name='chart'),
    path('results/', views.results_page, name='results'),
    path('perspective/', views.perspective_page, name='perspective'),
    path('visiting-famous-faces/', views.visiting_famous_page, name='visiting-famous'),
    path('patient-chart/', views.patient_chart_page, name='patient-chart'),
    path('committees/', views.committees_page, name='committees'),
    path('credit/', views.credit_page, name='credit'),
    path('quality-improvement/', views.quality_improvement_page, name='quality-improvement'),
    path('deceaseds/', views.deceaseds_page, name='deceaseds'),

    # patient guidence tab

]