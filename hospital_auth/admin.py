from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    User, 
    PatientModel,
    LoginCodeModel,
    UserFullNameModel
)


class AdminUser(UserAdmin):
    UserAdmin.fieldsets[1][1]['fields'] = (
        # 'first_name',
        # 'last_name',
        'phone',
        'gender',
        'profile',
        'age',
    )
    UserAdmin.fieldsets[2][1]['fields'] = (
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
        # 'user_permissions',
        'is_doctor_manager',
        'is_blog_manager',
        'is_news_manager',
        'is_note_manager',
        'is_expriment_manager',
        'is_appointment_manager',
        'is_contact_manager',
        'is_ipd_manager',
    )
    list_display = ('id', 'username', 'get_full_name', 'phone')
    ordering = ['-id']


class UserFullNameModel_Admin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name']
    ordering = ['-id']


class PatientModel_Admin(admin.ModelAdmin):
    list_display = ['username', 'gender', 'age']
    search_field = ['username', 'gender', 'age']
    ordering = ['-id']


class LoginCodeModel_Admin(admin.ModelAdmin):
    list_display = ['user', 'code', 'j_date', 'j_expire', 'is_use']
    search_field = ['is_use', 'user']
    ordering = ['-id']


admin.site.register(User, AdminUser)
admin.site.register(UserFullNameModel, UserFullNameModel_Admin)
admin.site.register(PatientModel, PatientModel_Admin)
admin.site.register(LoginCodeModel, LoginCodeModel_Admin)

admin.site.site_header = _('پنل ادمین بیمارستان موسی ابن جعفر')