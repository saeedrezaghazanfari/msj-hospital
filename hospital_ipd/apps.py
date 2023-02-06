from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HospitalIpdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_ipd'
    verbose_name = _('ماژول IPD')
