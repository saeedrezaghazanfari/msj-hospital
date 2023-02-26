from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    SettingModel,
    CostModel,
    HospitalPoliticModel,
    HospitalFacilityModel,
    FAQModel,
    NewsLetterEmailsModel,
    InsuranceModel,
    HospitalImageGalleryModel,
    HospitalImageGalleryItemModel,
    HospitalVideoGalleryModel,
    HospitalVideoGalleryItemModel,
    ReportModel,
    PriceAppointmentModel,
    ResultModel,
    HomeGalleryModel,
    CertificateModel,
    ContactInfoModel,
    PriceServiceModel,
    PriceBedModel,
    PriceSurgrayModel,
    AncientsModel
)


class SettingModel_Admin(admin.ModelAdmin):
    list_display = ['id', '__str__']


class CostModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class HospitalPoliticModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class HospitalFacilityModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class FAQModel_Admin(admin.ModelAdmin):
    list_display = ['question']
    search_field = ['question']
    ordering = ['-id']


class NewsLetterEmailsModel_Admin(admin.ModelAdmin):
    list_display = ['email']
    search_field = ['email']
    ordering = ['-id']


class InsuranceModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class HospitalGalleries_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']


class ReportModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'time_bound']
    search_field = ['time_bound']
    ordering = ['-id']


class PriceAppointmentModel_Admin(admin.ModelAdmin):
    list_display = ['degree', 'insurance', 'price']
    search_field = ['degree', 'insurance']
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
    list_display = ['title', 'insurance', 'price_free', 'price_insurance']
    search_field = ['title']
    ordering = ['-id']


class PriceSurgrayModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'insurance', 'price_free', 'price_insurance']
    search_field = ['title']
    ordering = ['-id']


class AncientsModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'full_name']
    ordering = ['-id']


admin.site.register(SettingModel, SettingModel_Admin)
admin.site.register(CostModel, CostModel_Admin)
admin.site.register(HospitalPoliticModel, HospitalPoliticModel_Admin)
admin.site.register(HospitalFacilityModel, HospitalFacilityModel_Admin)
admin.site.register(FAQModel, FAQModel_Admin)
admin.site.register(NewsLetterEmailsModel, NewsLetterEmailsModel_Admin)
admin.site.register(InsuranceModel, InsuranceModel_Admin)
admin.site.register(HospitalImageGalleryModel, HospitalGalleries_Admin)
admin.site.register(HospitalImageGalleryItemModel, HospitalGalleries_Admin)
admin.site.register(HospitalVideoGalleryModel, HospitalGalleries_Admin)
admin.site.register(HospitalVideoGalleryItemModel, HospitalGalleries_Admin)
admin.site.register(ReportModel, ReportModel_Admin)
admin.site.register(PriceAppointmentModel, PriceAppointmentModel_Admin)
admin.site.register(ResultModel, ResultModel_Admin)
admin.site.register(HomeGalleryModel, HomeGalleryModel_Admin)
admin.site.register(CertificateModel, CertificateModel_Admin)
admin.site.register(ContactInfoModel, ContactInfoModel_Admin)
admin.site.register(PriceServiceModel, PriceServiceModel_Admin)
admin.site.register(PriceBedModel, PriceBedModel_Admin)
admin.site.register(PriceSurgrayModel, PriceSurgrayModel_Admin)
admin.site.register(AncientsModel, AncientsModel_Admin)