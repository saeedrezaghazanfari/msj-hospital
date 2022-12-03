from django.contrib import admin
from .models import (
    ClinicModel,
    SurgeryRoomModel,
    DepartmentModel,
    TreatmentSectionModel,
    ParaclinicModel,
    ImagingModel,
    LaboratoryModel,
    PhysiotherapyModel,
    PharmacyModel,
    AngiographyAngioplastyModel,
    EmergencyModel,
)


class ShowData_Admin(admin.ModelAdmin):
    list_display = ['title', 'inside']
    search_fields = ['title', 'inside']
    ordering = ['-id']


admin.site.register(ClinicModel, ShowData_Admin)
admin.site.register(SurgeryRoomModel, ShowData_Admin)
admin.site.register(DepartmentModel, ShowData_Admin)
admin.site.register(TreatmentSectionModel, ShowData_Admin)
admin.site.register(ParaclinicModel, ShowData_Admin)
admin.site.register(ImagingModel, ShowData_Admin)
admin.site.register(LaboratoryModel, ShowData_Admin)
admin.site.register(PhysiotherapyModel, ShowData_Admin)
admin.site.register(PharmacyModel, ShowData_Admin)
admin.site.register(AngiographyAngioplastyModel, ShowData_Admin)
admin.site.register(EmergencyModel, ShowData_Admin)