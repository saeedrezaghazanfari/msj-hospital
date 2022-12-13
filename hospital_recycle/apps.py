from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HospitalRecycleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_recycle'
    verbose_name = _('بازیابی اطلاعات')
