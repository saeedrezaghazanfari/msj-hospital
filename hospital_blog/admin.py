from django.contrib import admin
from .models import (
    MedicalNoteModel,
    SMSTextModel,
    PampheletModel,
    CreditEduModel,
    BlogModel,
    BlogGalleryModel,
    BlogCommentModel,
    CategoryModel,
    TagModel,
    BlogLikeModel,
)


class MedicalNoteModel_Admin(admin.ModelAdmin):
    list_display = ['text', 'is_active']
    search_fields = ['text']
    ordering = ['-id']


class SMSTextModel_Admin(admin.ModelAdmin):
    list_display = ['receivers', 'is_sent_sms']
    search_fields = ['receivers']
    ordering = ['-created']


class PampheletModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['-id']


class CreditEduModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['-id']


class BlogModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_full_name', 'is_publish', 'is_emailed']
    ordering = ['-id']


class BlogGalleryModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['-id']


class BlogCommentModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'reply', 'is_show', 'is_read', 'j_created']
    ordering = ['-id']


class CategoryModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['-id']


class TagModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['-id']


class BlogLikeModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'like_dislike']
    ordering = ['-id']


admin.site.register(MedicalNoteModel, MedicalNoteModel_Admin)
admin.site.register(SMSTextModel, SMSTextModel_Admin)
admin.site.register(PampheletModel, PampheletModel_Admin)
admin.site.register(CreditEduModel, CreditEduModel_Admin)
admin.site.register(BlogModel, BlogModel_Admin)
admin.site.register(BlogGalleryModel, BlogGalleryModel_Admin)
admin.site.register(BlogCommentModel, BlogCommentModel_Admin)
admin.site.register(CategoryModel, CategoryModel_Admin)
admin.site.register(TagModel, TagModel_Admin)
admin.site.register(BlogLikeModel, BlogLikeModel_Admin)