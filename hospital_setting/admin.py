from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    SettingModel,
    CostModel,
    HospitalPoliticModel, HospitalPoliticRECYCLE,
    HospitalFacilityModel,
    FAQModel,
    NewsLetterModel,
    InsuranceModel,
    HospitalGalleryModel,
    HospitalGalleryItemModel,
    ReportModel,
    PriceAppointmentModel,
    ResultModel,
    HomeGalleryModel,
    CertificateModel,
    ContactInfoModel,
    PriceServiceModel,
    PriceBedModel,
    PriceSurgrayModel
)


class SettingModel_Admin(admin.ModelAdmin):
    list_display = ['id', '__str__']


class CostModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'year']
    search_field = ['title', 'year']
    ordering = ['-id']


class HospitalPoliticModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']

class HospitalPoliticRECYCLE_Admin(admin.ModelAdmin):

    actions = ['recover']

    def get_queryset(self, request):
        return HospitalPoliticRECYCLE.deleted.filter(is_deleted=True)

    @admin.action(description=_('ریکاوری کردن'))
    def recover(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)


class HospitalFacilityModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class FAQModel_Admin(admin.ModelAdmin):
    list_display = ['question']
    search_field = ['question']
    ordering = ['-id']


class NewsLetterModel_Admin(admin.ModelAdmin):
    list_display = ['email']
    search_field = ['email']
    ordering = ['-id']


class InsuranceModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class HospitalGalleryModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class HospitalGalleryItemModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'file_type']
    search_field = ['title', 'file_type']
    ordering = ['-id']


class ReportModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'time_bound']
    search_field = ['time_bound']
    ordering = ['-id']


class PriceAppointmentModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'degree', 'insurance', 'price_free', 'price_insurance']
    search_field = ['title', 'degree', 'insurance']
    ordering = ['-id']


class ResultModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class HomeGalleryModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class CertificateModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class ContactInfoModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class PriceServiceModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class PriceBedModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class PriceSurgrayModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


admin.site.register(SettingModel, SettingModel_Admin)
admin.site.register(CostModel, CostModel_Admin)
admin.site.register(HospitalPoliticModel, HospitalPoliticModel_Admin)
admin.site.register(HospitalPoliticRECYCLE, HospitalPoliticRECYCLE_Admin)

admin.site.register(HospitalFacilityModel, HospitalFacilityModel_Admin)
admin.site.register(FAQModel, FAQModel_Admin)
admin.site.register(NewsLetterModel, NewsLetterModel_Admin)
admin.site.register(InsuranceModel, InsuranceModel_Admin)
admin.site.register(HospitalGalleryModel, HospitalGalleryModel_Admin)
admin.site.register(HospitalGalleryItemModel, HospitalGalleryItemModel_Admin)
admin.site.register(ReportModel, ReportModel_Admin)
admin.site.register(PriceAppointmentModel, PriceAppointmentModel_Admin)
admin.site.register(ResultModel, ResultModel_Admin)
admin.site.register(HomeGalleryModel, HomeGalleryModel_Admin)
admin.site.register(CertificateModel, CertificateModel_Admin)
admin.site.register(ContactInfoModel, ContactInfoModel_Admin)
admin.site.register(PriceServiceModel, PriceServiceModel_Admin)
admin.site.register(PriceBedModel, PriceBedModel_Admin)
admin.site.register(PriceSurgrayModel, PriceSurgrayModel_Admin)