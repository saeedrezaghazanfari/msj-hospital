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
    path('board-of-directors/', views.board_of_directors_page, name='board-of-directors'),
    path('ceo-management/', views.ceo_management_page, name='ceo-management'),
    path('chart/', views.chart_page, name='chart'),
    path('results/', views.results_page, name='results'),
    path('perspective/', views.perspective_page, name='perspective'),
    path('visiting-famous-faces/', views.visiting_famous_page, name='visiting-famous'),
    path('patient/chart/', views.patient_chart_page, name='patient-chart'),
    path('patient/edu/', views.patient_edu_page, name='patient-edu'),
    path('committees/', views.committees_page, name='committees'),
    path('credit/', views.credit_page, name='credit'),
    path('quality-improvement/', views.quality_improvement_page, name='quality-improvement'),
    path('deceaseds/', views.deceaseds_page, name='deceaseds'),
    path('benefactors/', views.benefactors_page, name='benefactors'),
    path('facility/', views.facility_page, name='facility'),
    path('reports/', views.reports_page, name='reports'),

    # patient guidence tab
    path('clinic/program/', views.clinic_program_page, name='clinic-program'),
    path('prices/', views.prices_page, name='prices'),
    path('prices/bed/', views.prices_bed_page, name='prices-bed'),
    path('prices/services/', views.prices_services_page, name='prices-services'),
    path('prices/surgray/', views.prices_surgray_page, name='prices-surgray'),
    path('insurances/', views.insurances_page, name='insurances'),
    path('phones/', views.phones_page, name='phones'),
    path('visitors-guide/', views.visitors_guide_page, name='visitors-guide'),

    # services tab
    path('clinic/list/', views.clinic_list_page, name='clinic-list'),
    path('unit/<unitId>/', views.unit_page, name='unit-info'),

]