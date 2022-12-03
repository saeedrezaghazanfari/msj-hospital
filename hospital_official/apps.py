from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HospitalOfficialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_official'
    verbose_name = _('ماژول اداری')