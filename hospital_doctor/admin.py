from django.contrib import admin
from .models import (
    DoctorModel,
    DoctorSkillModel,
    TitleSkillModel,
    DoctorWorkTimeModel,
    DoctorVacationModel,
)


class DoctorModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name']
    ordering = ['-id']


class DoctorSkillModel_Admin(admin.ModelAdmin):
    list_display = ['medical_code', 'doctor', 'is_active']
    search_fields = ['medical_code']
    ordering = ['-id']


class TitleSkillModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    ordering = ['-id']


class DoctorWorkTimeModel_Admin(admin.ModelAdmin):
    list_display = ['doctor', 'day', 'time']
    search_fields = ['doctor', 'day', 'time']
    ordering = ['-id']


class DoctorVacationModel_Admin(admin.ModelAdmin):
    list_display = ['doctor', 'from_time', 'to_time']
    search_fields = ['doctor']
    ordering = ['-id']


admin.site.register(DoctorModel, DoctorModel_Admin)
admin.site.register(DoctorSkillModel, DoctorSkillModel_Admin)
admin.site.register(TitleSkillModel, TitleSkillModel_Admin)
admin.site.register(DoctorWorkTimeModel, DoctorWorkTimeModel_Admin)
admin.site.register(DoctorVacationModel, DoctorVacationModel_Admin)