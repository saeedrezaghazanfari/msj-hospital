from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from hospital_auth.models import User
from hospital_units.models import ClinicModel


# class AppoListModel(models.Model):
#     medical_code = models.BigIntegerField(verbose_name=_('کد نظام پزشکی'))
#     skill_title = models.ForeignKey('TitleSkillModel', on_delete=models.CASCADE, verbose_name=_('عنوان تخصص'))
#     user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
#     clinic = models.ForeignKey(to=ClinicModel, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('کلینیک'))
#     position = models.TextField(max_length=500, null=True, blank=True, verbose_name=_('موقعیت'))
#     description = models.TextField(blank=True, null=True, verbose_name=_('توضیحات'))
#     bio = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('بیوگرافی'))
#     is_active = models.BooleanField(default=False, verbose_name=_('فعال/غیرفعال'))

#     class Meta:
#         ordering = ['-id']
#         verbose_name = _('پزشک')
#         verbose_name_plural = _('پزشکان')

#     def __str__(self):
#         return self.title

#     def get_full_name(self):
#         return f'{self.user.first_name} {self.user.last_name}'
#     get_full_name.short_description = _('نام پزشک')