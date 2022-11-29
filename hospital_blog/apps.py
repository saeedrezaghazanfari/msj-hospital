from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HospitalBlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_blog'
    verbose_name = _('ماژول بلاگ و اخبار')
