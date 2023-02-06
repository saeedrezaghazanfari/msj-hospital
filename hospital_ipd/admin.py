from django.contrib import admin
from .models import (
    IPDModel, IPDCodeModel
)


class IPDModel_Admin(admin.ModelAdmin):
    list_display = ['get_full_name']
    ordering = ['-id']

class IPDCodeModel_Admin(admin.ModelAdmin):
    list_display = ['ipd', 'code', 'j_date', 'j_expire', 'is_use']
    search_field = ['is_use', 'ipd']
    ordering = ['-id']


admin.site.register(IPDModel, IPDModel_Admin)
admin.site.register(IPDCodeModel, IPDCodeModel_Admin)