from django.contrib import admin
from .models import (
    SettingModel,
    CostModel,
    HospitalPoliticModel,
    HospitalFacilityModel,
    FAQModel,
    NewsLetterModel,
    InsuranceModel,
    HospitalGalleryModel,
    HospitalGalleryItemModel,
    ReportModel,
    PriceModel,
    ResultModel,
    HomeGalleryModel,
    CertificateModel,
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


class PriceModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'price']
    search_field = ['title', 'price']
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


admin.site.register(SettingModel, SettingModel_Admin)
admin.site.register(CostModel, CostModel_Admin)
admin.site.register(HospitalPoliticModel, HospitalPoliticModel_Admin)
admin.site.register(HospitalFacilityModel, HospitalFacilityModel_Admin)
admin.site.register(FAQModel, FAQModel_Admin)
admin.site.register(NewsLetterModel, NewsLetterModel_Admin)
admin.site.register(InsuranceModel, InsuranceModel_Admin)
admin.site.register(HospitalGalleryModel, HospitalGalleryModel_Admin)
admin.site.register(HospitalGalleryItemModel, HospitalGalleryItemModel_Admin)
admin.site.register(ReportModel, ReportModel_Admin)
admin.site.register(PriceModel, PriceModel_Admin)
admin.site.register(ResultModel, ResultModel_Admin)
admin.site.register(HomeGalleryModel, HomeGalleryModel_Admin)
admin.site.register(CertificateModel, CertificateModel_Admin)
