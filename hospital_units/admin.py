from django.contrib import admin
from .models import (
    UnitModel, 
    SubUnitModel,
    UnitMemberModel,
    ExprimentResultModel,
    AppointmentTimeModel,
    AppointmentTipModel,
    PatientTurnModel,
    OnlinePaymentModel,
    LimitTurnTimeModel
)


class UnitModel_Admin(admin.ModelAdmin):
    list_display = ['category', 'subunit', 'title']
    search_fields = ['category', 'subunit', 'title']
    ordering = ['-id']


class SubUnitModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    ordering = ['-id']


class UnitMemberModel_Admin(admin.ModelAdmin):
    list_display = ['__str__', 'job']
    ordering = ['-id']


class ExprimentResultModel_Admin(admin.ModelAdmin):
    list_display = ['code', 'type', 'patient', 'unit']
    search_fields = ['code', 'type', 'patient', 'unit']
    ordering = ['-id']


class AppointmentTimeModel_Admin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'day', 'time_from', 'time_to', 'capacity', 'reserved']
    search_fields = ['doctor', 'date', 'day']
    ordering = ['-id']


class AppointmentTipModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['-id']


class PatientTurnModel_Admin(admin.ModelAdmin):
    list_display = ['code', 'appointment', 'first_name', 'last_name', 'national_code']
    search_fields = ['code', 'appointment', 'first_name', 'last_name', 'national_code']
    ordering = ['-id']

class OnlinePaymentModel_Admin(admin.ModelAdmin):
    list_display = ['payer', 'price', 'is_success', 'code']
    search_fields = ['payer', 'price', 'code']
    ordering = ['-id']


class LimitTurnTimeModel_Admin(admin.ModelAdmin):
    list_display = ['__str__']
    ordering = ['-id']


admin.site.register(UnitModel, UnitModel_Admin)
admin.site.register(SubUnitModel, SubUnitModel_Admin)
admin.site.register(UnitMemberModel, UnitMemberModel_Admin)
admin.site.register(ExprimentResultModel, ExprimentResultModel_Admin)
admin.site.register(AppointmentTimeModel, AppointmentTimeModel_Admin)
admin.site.register(AppointmentTipModel, AppointmentTipModel_Admin)
admin.site.register(PatientTurnModel, PatientTurnModel_Admin)
admin.site.register(OnlinePaymentModel, OnlinePaymentModel_Admin)
admin.site.register(LimitTurnTimeModel, LimitTurnTimeModel_Admin)