from django.contrib import admin
from .models import OrganModel, OrganItemModel


class OrganModel_Admin(admin.ModelAdmin):
    list_display = ['type']
    search_fields = ['type']
    ordering = ['-id']


class OrganItemModel_Admin(admin.ModelAdmin):
    list_display = ['organ', '__str__', 'job']
    search_fields = ['organ', 'job']
    ordering = ['-id']


admin.site.register(OrganModel, OrganModel_Admin)
admin.site.register(OrganItemModel, OrganItemModel_Admin)