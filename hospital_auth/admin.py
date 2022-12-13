from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import (
    User, 
    LoginCodeModel, 
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
        'is_blog_manager',
        'is_news_manager',
        'is_note_manager',
        'is_expriment_manager',
        'is_appointment_manager',
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