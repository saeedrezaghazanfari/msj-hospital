from django.contrib import admin
from .models import (
    UnitModel, 
    SubUnitModel,
    UnitMemberModel,
    ManagersModel,
    ExprimentResultModel,
    AppointmentTimeModel,
    AppointmentTipModel,
    AppointmentTipSMSModel,
    PatientTurnModel,
    ElectronicPrescriptionModel,
    OnlinePaymentModel,
    LimitTurnTimeModel,
    LoginCodePatientModel
)


class UnitModel_Admin(admin.ModelAdmin):
    list_display = ['subunit', 'title']
    search_fields = ['subunit', 'title']
    ordering = ['-id']


class SubUnitModel_Admin(admin.ModelAdmin):
    list_display = ['slug', 'category', 'title', 'have_2_box']
    search_fields = ['slug', 'category', 'title', 'have_2_box']
    ordering = ['-id']


class UnitMemberModel_Admin(admin.ModelAdmin):
    list_display = ['__str__', 'job']
    ordering = ['-id']


class ManagersModel_Admin(admin.ModelAdmin):
    list_display = ['__str__', 'job']
    ordering = ['-id']


class ExprimentResultModel_Admin(admin.ModelAdmin):
    list_display = ['code', 'patient', 'unit']
    search_fields = ['code', 'patient', 'unit']
    ordering = ['-id']


class AppointmentTimeModel_Admin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'day', 'time_from', 'time_to', 'capacity', 'reserved']
    search_fields = ['doctor', 'date', 'day']
    ordering = ['date']


class AppointmentTipModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['-id']


class PatientTurnModel_Admin(admin.ModelAdmin):
    list_display = ['code', 'appointment', 'patient']
    search_fields = ['code', 'appointment']
    ordering = ['-id']

class ElectronicPrescriptionModel_Admin(admin.ModelAdmin):
    list_display = ['patient', 'unit', 'is_send']
    search_fields = ['patient', 'unit', 'is_send']
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
admin.site.register(ManagersModel, ManagersModel_Admin)
admin.site.register(ExprimentResultModel, ExprimentResultModel_Admin)
admin.site.register(AppointmentTimeModel, AppointmentTimeModel_Admin)
admin.site.register(AppointmentTipModel, AppointmentTipModel_Admin)
admin.site.register(AppointmentTipSMSModel, AppointmentTipModel_Admin)
admin.site.register(PatientTurnModel, PatientTurnModel_Admin)
admin.site.register(ElectronicPrescriptionModel, ElectronicPrescriptionModel_Admin)
admin.site.register(OnlinePaymentModel, OnlinePaymentModel_Admin)
admin.site.register(LimitTurnTimeModel, LimitTurnTimeModel_Admin)
admin.site.register(LoginCodePatientModel)