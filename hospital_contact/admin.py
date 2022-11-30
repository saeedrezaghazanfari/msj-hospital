from django.contrib import admin
from .models import (
    NotificationModel,
    NotificationUserModel,
    # PatientSightModel,
    # CooperationModel,
    ContactUsModel,
    # CriticismSuggestionModel,
    PeopleAidModel,
    BenefactorModel,
)


class NotificationModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'is_from_boss', 'j_publish_time']
    search_fields = ['title']
    ordering = ['-id']


class NotificationUserModel_Admin(admin.ModelAdmin):
    list_display = ['id']
    ordering = ['-id']


# class PatientSightModel_Admin(admin.ModelAdmin):
#     list_display = []
#     search_fields = []
#     ordering = ['-id']


# class CooperationModel_Admin(admin.ModelAdmin):
#     list_display = []
#     search_fields = []
#     ordering = ['-id']


class ContactUsModel_Admin(admin.ModelAdmin):
    list_display = ['name', 'is_read', 'j_created']
    search_fields = ['name']
    ordering = ['-id']


# class CriticismSuggestionModel_Admin(admin.ModelAdmin):
#     list_display = []
#     search_fields = []
#     ordering = ['-id']


class PeopleAidModel_Admin(admin.ModelAdmin):
    list_display = ['name', 'price', 'j_date_of_aid']
    search_fields = ['name']
    ordering = ['-id']


class BenefactorModel_Admin(admin.ModelAdmin):
    list_display = ['name', 'is_founder']
    search_fields = ['name']
    ordering = ['-id']


admin.site.register(NotificationModel, NotificationModel_Admin)
admin.site.register(NotificationUserModel, NotificationUserModel_Admin)
# admin.site.register(PatientSightModel, PatientSightModel_Admin)
# admin.site.register(CooperationModel, CooperationModel_Admin)
admin.site.register(ContactUsModel, ContactUsModel_Admin)
# admin.site.register(CriticismSuggestionModel, CriticismSuggestionModel_Admin)
admin.site.register(PeopleAidModel, PeopleAidModel_Admin)
admin.site.register(BenefactorModel, BenefactorModel_Admin)