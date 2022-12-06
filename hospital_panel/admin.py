from django.contrib import admin
from .models import (
    AppointmentTimeListModel,
    PatientTurnModel,
    UserElectronicPaymentModel,
)


class AppointmentTimeListModel_Admin(admin.ModelAdmin):
    list_display = ['part_name', 'doctor', 'j_date', 'time']
    search_fields = ['part_name', 'doctor', 'j_date', 'time']
    ordering = ['-id']


class PatientTurnModel_Admin(admin.ModelAdmin):
    list_display = ['tracking_code', 'full_name', 'is_visited', 'is_paid', 'j_created']
    search_fields = ['tracking_code', 'j_created']
    ordering = ['-id']


class UserElectronicPaymentModel_Admin(admin.ModelAdmin):
    list_display = ['user', 'price', 'is_success', 'j_created']
    search_fields = ['user', 'is_success']
    ordering = ['-id']


admin.site.register(AppointmentTimeListModel, AppointmentTimeListModel_Admin)
admin.site.register(PatientTurnModel, PatientTurnModel_Admin)
admin.site.register(UserElectronicPaymentModel, UserElectronicPaymentModel_Admin)