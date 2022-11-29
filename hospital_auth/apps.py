from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HospitalAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_auth'
    verbose_name = _('احراز هویت')