from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('blog/blogs/', views.list_page, name='blogs'),
]