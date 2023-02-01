from django.urls import path
from . import (
    views, views_appointment, views_doctor, views_contacts,
    views_experiment, views_blog, views_news, views_notes
)


app_name = 'panel'
urlpatterns = [
    
    # Real pathes
    path('panel/', views.home_page, name='home'),
    path('panel/read/notification/<notificationID>/', views.read_notification, name='read-notif'),
    path('panel/edit-info/', views.edit_data, name='editdata'),
    path('panel/edit-info/fullname/', views.edit_fullname, name='editdata-fullname'),


    # doctor management
    path('panel/doctor/', views_doctor.doctor_page, name='doctor'),
    path('panel/doctor/info/', views_doctor.doctor_info_page, name='doctor-info'),
    path('panel/doctor/vacation/', views_doctor.doctor_vacation_page, name='doctor-vacation'),
    path('panel/doctor/work/', views_doctor.doctor_work_page, name='doctor-work'),
    path('panel/doctor/insurances/', views_doctor.doctor_insurances_page, name='doctor-insurances'),
    path('panel/doctor/patients/', views_doctor.doctor_patients_page, name='doctor-patients'),


    # contact management
    path('panel/contact/', views_contacts.contact_page, name='contact'),
    path('panel/contact/careers/', views_contacts.contact_careers_page, name='contact-careers'),
    path('panel/contact/careers/edit/<careerCode>/', views_contacts.contact_career_edit_page, name='contact-careeredit'),
    path('panel/contact/recruitations/', views_contacts.contact_recruitations_page, name='contact-recruitations'),
    path('panel/contact/recruitations/info/<hireId>/', views_contacts.contact_recruitations_info_page, name='contact-recruitationsinfo'),
    path('panel/contact/suggestions/', views_contacts.contact_suggestions_page, name='contact-suggestions'),
    path('panel/contact/suggestions/info/<suggestionCode>/', views_contacts.contact_suggestions_info_page, name='contact-suggestionsinfo'),
    path('panel/contact/contacts/', views_contacts.contact_contacts_page, name='contact-contacts'),
    path('panel/contact/contacts/info/<contactId>/', views_contacts.contact_contacts_info_page, name='contact-contactsinfo'),


    # blog management
    path('panel/blog/', views_blog.blog_page, name='blog-list'),
    path('panel/blog/create/', views_blog.blog_create_page, name='blog-create'),
    path('panel/blog/edit/<blogSlug>/', views_blog.blog_edit_page, name='blog-edit'),
    path('panel/blog/tag/', views_blog.blog_tag_page, name='blog-tag'),
    path('panel/blog/category/', views_blog.blog_category_page, name='blog-category'),
    path('panel/blog/gallery/', views_blog.blog_gallery_page, name='blog-gallery'),
    path('panel/blog/comment/', views_blog.blog_comment_page, name='blog-comments'),
    path('panel/blog/pamphlet/', views_blog.blog_pamphlet_page, name='blog-pamphlet'),
    path('panel/blog/comment/read/<commentId>/', views_blog.blog_comment_read_page, name='blog-commentread'),
    path('panel/blog/comment/show/<commentId>/', views_blog.blog_comment_show_page, name='blog-commentshow'),
    path('panel/blog/comment/delete/<commentId>/', views_blog.blog_comment_delete_page, name='blog-commentdelete'),
    path('panel/blog/comment/edit/<commentId>/', views_blog.blog_comment_edit_page, name='blog-commentedit'),


    # news management
    path('panel/news/', views_news.news_page, name='news-list'),
    path('panel/news/create/', views_news.news_create_page, name='news-create'),
    path('panel/news/edit/<newsSlug>/', views_news.news_edit_page, name='news-edit'),
    path('panel/news/tag/', views_news.news_tag_page, name='news-tag'),
    path('panel/news/category/', views_news.news_category_page, name='news-category'),
    path('panel/news/gallery/', views_news.news_gallery_page, name='news-gallery'),
    path('panel/news/comment/', views_news.news_comment_page, name='news-comments'),
    path('panel/news/comment/read/<commentId>/', views_news.news_comment_read_page, name='news-commentread'),
    path('panel/news/comment/show/<commentId>/', views_news.news_comment_show_page, name='news-commentshow'),
    path('panel/news/comment/delete/<commentId>/', views_news.news_comment_delete_page, name='news-commentdelete'),
    path('panel/news/comment/edit/<commentId>/', views_news.news_comment_edit_page, name='news-commentedit'),


    # note management
    path('panel/notes/', views_notes.notes_page, name='notes-list'),
    path('panel/notes/<noteId>/', views_notes.notes_edit_page, name='notes-edit'),


    # experiment management
    path('panel/experiment/', views_experiment.experiment_page, name='experiment'),
    path('panel/experiment/list/', views_experiment.experiment_list_page, name='experiment-list'),
    path('panel/experiment/patient/', views_experiment.experiment_patient_page, name='experiment-patient'),


    # online appointment management
    path('panel/online-appointment/missions/lvl1/', views_appointment.oa_mission_1, name='mission-1'),
    path('panel/online-appointment/missions/lvl2/', views_appointment.oa_mission_2, name='mission-2'),
    path('panel/online-appointment/missions/lvl3/', views_appointment.oa_mission_3, name='mission-3'),
    path('panel/online-appointment/missions/lvl4/', views_appointment.oa_mission_4, name='mission-4'),
    path('panel/online-appointment/missions/lvl5/', views_appointment.oa_mission_5, name='mission-5'),
    path('panel/online-appointment/missions/lvl6/', views_appointment.oa_mission_6, name='mission-6'),

    path('panel/online-appointment/', views_appointment.online_appointment_page, name='appointment'),
    path('panel/online-appointment/limit-time/', views_appointment.oa_limit_time_page, name='appointment-limittime'),
    path('panel/online-appointment/insurances/', views_appointment.oa_insurances_page, name='appointment-insurances'),
    path('panel/online-appointment/tips/', views_appointment.oa_tips_page, name='appointment-tips'),
    path('panel/online-appointment/tips/sms/', views_appointment.oa_smstips_page, name='appointment-smstips'),
    path('panel/online-appointment/skill/', views_appointment.oa_skilltitle_page, name='appointment-skill'),
    path('panel/online-appointment/degree/', views_appointment.oa_degree_page, name='appointment-degree'),
    path('panel/online-appointment/unit/', views_appointment.oa_unit_page, name='appointment-unit'),
    path('panel/online-appointment/subunit/', views_appointment.oa_subunit_page, name='appointment-subunit'),
    path('panel/online-appointment/doctor/list/', views_appointment.oa_doctorlist_page, name='appointment-doctorlist'),
    path('panel/online-appointment/doctor/create/', views_appointment.oa_doctorcreate_page, name='appointment-doctorcreate'),
    path('panel/online-appointment/doctor/<doctorId>/times/', views_appointment.oa_doctorlist_time_page, name='appointment-doctorlist-times'),
    path('panel/online-appointment/doctor/<doctorId>/edit/', views_appointment.oa_doctorlist_edit_page, name='appointment-doctorlist-edit'),
    path('panel/online-appointment/price/', views_appointment.oa_price_page, name='appointment-price'),
    path('panel/online-appointment/time/', views_appointment.oa_time_page, name='appointment-time'),
    path('panel/online-appointment/time/<appointmentID>/edit/', views_appointment.oa_time_edit_page, name='appointment-timeedit'),
    path('panel/online-appointment/time/create/', views_appointment.oa_time_create0_page, name='appointment-timep0'),
    path('panel/online-appointment/time/create/<unitID>/', views_appointment.oa_time_create1_page, name='appointment-timep1'),
    path('panel/online-appointment/time/create/<unitID>/<doctorId>/', views_appointment.oa_time_create2_page, name='appointment-timep2'),
    path('panel/online-appointment/patient/', views_appointment.oa_patient_page, name='appointment-patient'),
    path('panel/online-appointment/e-turn/', views_appointment.oa_eturn_list_page, name='appointment-eturnlist'),
    path('panel/online-appointment/e-turn/<eturnID>/', views_appointment.oa_eturn_check_page, name='appointment-eturncheck'),
]