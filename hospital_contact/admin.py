from django.contrib import admin
from .models import (
    NotificationModel,
    PatientSightModel,
    BeneficiaryCommentModel,
    ContactUsModel,
    CriticismSuggestionModel,
    PeopleAidModel,
    BenefactorModel,
    CareersModel,
    HireFormModel,
    WorkshopModel,
    FamousPatientModel
)


class NotificationModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'is_from_boss', 'is_published', 'user']
    search_fields = ['title']
    ordering = ['-id']


class PatientSightModel_Admin(admin.ModelAdmin):
    list_display = ['patient', 'unit']
    search_fields = ['patient', 'unit']
    ordering = ['-id']


class BeneficiaryCommentModel_Admin(admin.ModelAdmin):
    list_display = ['__str__']
    ordering = ['-id']


class ContactUsModel_Admin(admin.ModelAdmin):
    list_display = ['name', 'is_read', 'j_created']
    search_fields = ['name']
    ordering = ['-id']


class CriticismSuggestionModel_Admin(admin.ModelAdmin):
    list_display = ['first_name', 'first_name', 'national_code', 'unit']
    search_fields = ['first_name', 'first_name', 'national_code']
    ordering = ['-id']


class PeopleAidModel_Admin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'j_date_of_aid']
    search_fields = ['__str__']
    ordering = ['-id']


class BenefactorModel_Admin(admin.ModelAdmin):
    list_display = ['__str__', 'is_founder']
    search_fields = ['__str__']
    ordering = ['-id']


class CareersModel_Admin(admin.ModelAdmin):
    list_display = ['code', 'title', 'skill', 'degree']
    search_fields = ['code', 'title', 'skill', 'degree']
    ordering = ['-id']


class HireFormModel_Admin(admin.ModelAdmin):
    list_display = ['national_code', 'career', 'is_checked']
    ordering = ['-id']


class WorkshopModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    ordering = ['-id']


class FamousPatientModel_Admin(admin.ModelAdmin):
    list_display = ['__str__']
    ordering = ['-id']


admin.site.register(NotificationModel, NotificationModel_Admin)
admin.site.register(PatientSightModel, PatientSightModel_Admin)
admin.site.register(BeneficiaryCommentModel, BeneficiaryCommentModel_Admin)
admin.site.register(ContactUsModel, ContactUsModel_Admin)
admin.site.register(CriticismSuggestionModel, CriticismSuggestionModel_Admin)
admin.site.register(PeopleAidModel, PeopleAidModel_Admin)
admin.site.register(BenefactorModel, BenefactorModel_Admin)
admin.site.register(CareersModel, CareersModel_Admin)
admin.site.register(HireFormModel, HireFormModel_Admin)
admin.site.register(WorkshopModel, WorkshopModel_Admin)
admin.site.register(FamousPatientModel, FamousPatientModel_Admin)
