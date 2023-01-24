from django.urls import path
from . import views


app_name = 'news'
urlpatterns = [
    path('news/list/', views.ListPage.as_view(), name='news'),
    path('news/info/<newsSlug>/', views.info_page, name='info'),
    path('news/like-dislike/', views.like_dislike_page, name='like-dislike'),
    path('news/search/tags/<query>/', views.SearchTag.as_view(), name='tags'),
    path('news/search/categories/<query>/', views.SearchCategory.as_view(), name='categories'),
]