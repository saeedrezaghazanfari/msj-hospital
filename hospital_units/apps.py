from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HospitalUnitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_units'
    verbose_name = _('ماژول واحدها و بخش ها')