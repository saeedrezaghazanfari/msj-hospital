from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User, LoginCodeModel


class AdminUser(UserAdmin):
    UserAdmin.fieldsets[1][1]['fields'] = (
        'first_name',
        'last_name',
        'phone',
        'profile',
        'wallet_balance',
        'is_send_sms',
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



admin.site.register(User, AdminUser)
admin.site.register(LoginCodeModel, LoginCodeModel_Admin)
admin.site.unregister(Group)