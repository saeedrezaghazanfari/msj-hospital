from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import (
    User, 
    LoginCodeModel, 
    SupporterModel, 
    ContentProducerModel, 
    AdmissionsAdminModel
)


class AdminUser(UserAdmin):
    UserAdmin.fieldsets[1][1]['fields'] = (
        'first_name',
        'last_name',
        'phone',
        'fixed_phone',
        'gender',
        'profile',
        'wallet_balance',
        'is_send_sms',
        'is_active2',
    )
    UserAdmin.fieldsets[2][1]['fields'] = (
        'is_active',
        'is_staff',
        'is_superuser',
        # 'groups',
        # 'user_permissions',
    )
    list_display = ('id', 'username', 'get_full_name', 'phone')
    ordering = ['-id']


class LoginCodeModel_Admin(admin.ModelAdmin):
    list_display = ['user', 'code', 'j_date', 'j_expire', 'is_use']
    search_field = ['is_use', 'user']
    ordering = ['-id']

class SupporterModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'is_active']
    search_field = ['get_full_name']
    ordering = ['-id']

class ContentProducerModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'is_active']
    search_field = ['get_full_name']
    ordering = ['-id']

class AdmissionsAdminModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'is_active']
    search_field = ['get_full_name']
    ordering = ['-id']


admin.site.register(User, AdminUser)
admin.site.register(LoginCodeModel, LoginCodeModel_Admin)
admin.site.register(SupporterModel, SupporterModel_Admin)
admin.site.register(ContentProducerModel, ContentProducerModel_Admin)
admin.site.register(AdmissionsAdminModel, AdmissionsAdminModel_Admin)
admin.site.unregister(Group)