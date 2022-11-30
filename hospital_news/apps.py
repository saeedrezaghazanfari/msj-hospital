from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HospitalNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_news'
    verbose_name = _('ماژول اخبار')