from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HospitalJobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_jobs'
    verbose_name = _('ماژول مشاغل')
