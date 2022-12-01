from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HospitalPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_panel'
    verbose_name = _('ماژول پنل کاربری')
