from django.contrib import admin
from .models import (
    UnitModel, 
    ExprimentResultModel,
    AppointmentTimeModel,
    PatientTurnModel,
    OnlinePaymentModel
)


class UnitModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'category']
    search_fields = ['title', 'category']
    ordering = ['-id']


class ExprimentResultModel_Admin(admin.ModelAdmin):
    list_display = ['code', 'type', 'user', 'unit']
    search_fields = ['code', 'type', 'user', 'unit']
    ordering = ['-id']


class AppointmentTimeModel_Admin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'day', 'time', 'capacity', 'reserved']
    search_fields = ['doctor', 'date', 'day']
    ordering = ['-id']


class PatientTurnModel_Admin(admin.ModelAdmin):
    list_display = ['code', 'appointment', 'full_name', 'national_code']
    search_fields = ['code', 'appointment', 'full_name', 'national_code']
    ordering = ['-id']

class OnlinePaymentModel_Admin(admin.ModelAdmin):
    list_display = ['payer', 'price', 'is_success', 'code']
    search_fields = ['payer', 'price', 'code']
    ordering = ['-id']


admin.site.register(UnitModel, UnitModel_Admin)
admin.site.register(ExprimentResultModel, ExprimentResultModel_Admin)
admin.site.register(AppointmentTimeModel, AppointmentTimeModel_Admin)
admin.site.register(PatientTurnModel, PatientTurnModel_Admin)
admin.site.register(OnlinePaymentModel, OnlinePaymentModel_Admin)