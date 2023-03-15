from django.contrib import admin
from .models import (
    IPDModel, IPDCodeModel
)


class IPDModel_Admin(admin.ModelAdmin):
    list_display = ['username', 'age', 'gender', 'country', 'is_answered', 'j_created']
    search_field = ['phone']
    ordering = ['-id']

class IPDCodeModel_Admin(admin.ModelAdmin):
    list_display = ['phone', 'code', 'j_date', 'j_expire', 'is_use']
    search_field = ['phone']
    ordering = ['-id']


admin.site.register(IPDModel, IPDModel_Admin)
admin.site.register(IPDCodeModel, IPDCodeModel_Admin)