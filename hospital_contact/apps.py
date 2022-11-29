from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HospitalContactConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_contact'
    verbose_name = _('ماژول ارتباطات')