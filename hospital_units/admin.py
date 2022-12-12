from django.contrib import admin
from .models import UnitModel, ExprimentResultModel


class UnitModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'category']
    search_fields = ['title', 'category']
    ordering = ['-id']


class ExprimentResultModel_Admin(admin.ModelAdmin):
    list_display = ['code', 'type', 'user', 'unit']
    search_fields = ['code', 'type', 'user', 'unit']
    ordering = ['-id']


admin.site.register(UnitModel, UnitModel_Admin)
admin.site.register(ExprimentResultModel, ExprimentResultModel_Admin)