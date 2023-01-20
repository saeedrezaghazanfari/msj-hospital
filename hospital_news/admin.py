from django.contrib import admin
from .models import (
    NewsModel,
    NewsGalleryModel,
    NewsCommentModel,
    NewsLikeModel,
)


class NewsModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_full_name', 'is_publish', 'is_emailed']
    search_fields = ['title']
    ordering = ['-id']


class NewsGalleryModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    ordering = ['-id']


class NewsCommentModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'is_show', 'is_read', 'j_created']
    search_fields = ['is_show', 'is_read']
    ordering = ['-id']


class NewsLikeModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'like_dislike']
    search_fields = ['like_dislike']
    ordering = ['-id']


admin.site.register(NewsModel, NewsModel_Admin)
admin.site.register(NewsGalleryModel, NewsGalleryModel_Admin)
admin.site.register(NewsCommentModel, NewsCommentModel_Admin)
admin.site.register(NewsLikeModel, NewsLikeModel_Admin)