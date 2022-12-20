from django.contrib import admin
from .models import (
    DoctorModel,
    DoctorInsuranceModel,
    TitleSkillModel,
    DoctorWorkTimeModel,
    DoctorVacationModel,
    DegreeModel,
    FamousPatientModel
)


class DoctorModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'degree', 'skill_title']
    ordering = ['-id']


class DoctorInsuranceModel_Admin(admin.ModelAdmin):
    list_display = ['__str__']
    ordering = ['-id']


class TitleSkillModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    ordering = ['-id']


class DegreeModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    ordering = ['-id']


class DoctorWorkTimeModel_Admin(admin.ModelAdmin):
    list_display = ['doctor', 'day_from', 'day_to', 'time_from', 'time_to']
    search_fields = ['doctor', 'day_from', 'day_to']
    ordering = ['-id']


class DoctorVacationModel_Admin(admin.ModelAdmin):
    list_display = ['doctor', 'from_time', 'to_time']
    search_fields = ['doctor']
    ordering = ['-id']


class FamousPatientModel_Admin(admin.ModelAdmin):
    list_display = ['__str__']
    ordering = ['-id']


admin.site.register(DoctorModel, DoctorModel_Admin)
admin.site.register(DoctorInsuranceModel, DoctorInsuranceModel_Admin)
admin.site.register(TitleSkillModel, TitleSkillModel_Admin)
admin.site.register(DoctorWorkTimeModel, DoctorWorkTimeModel_Admin)
admin.site.register(DoctorVacationModel, DoctorVacationModel_Admin)
admin.site.register(DegreeModel, DegreeModel_Admin)
admin.site.register(FamousPatientModel, FamousPatientModel_Admin)