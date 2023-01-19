from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('blog/blogs/', views.list_page, name='blogs'),
    path('blog/blogs/<blogSlug>/', views.info_page, name='info'),
]