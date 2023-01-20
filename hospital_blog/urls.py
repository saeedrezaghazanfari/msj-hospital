from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('blog/list/', views.ListPage.as_view(), name='blogs'),
    path('blog/info/<blogSlug>/', views.info_page, name='info'),
]