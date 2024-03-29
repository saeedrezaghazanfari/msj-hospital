import uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField
from hospital_auth.models import User
from hospital_units.models import UnitModel
from ckeditor.fields import RichTextField
from hospital_extentions.utils import DAYS, TIMES


class DoctorModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    medical_code = models.CharField(max_length=15, unique=True, verbose_name=_('کد نظام‌پزشکی'))
    skill_title = models.ForeignKey('TitleSkillModel', on_delete=models.SET_NULL, null=True, verbose_name=_('عنوان تخصص'))
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('کاربر'))
    unit = models.ForeignKey(to=UnitModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بخش'))
    insurances = models.ManyToManyField('hospital_setting.InsuranceModel', verbose_name=_('بیمه‌های طرف قرارداد'))
    degree = models.ForeignKey('DegreeModel', on_delete=models.SET_NULL, null=True, verbose_name=_('نوع مدرک'))
    position = TranslatedField(RichTextField(max_length=500, null=True, blank=True, verbose_name=_('موقعیت')))
    bio = TranslatedField(RichTextField(max_length=500, blank=True, null=True, verbose_name=_('بیوگرافی')))
    is_medicalteam = models.BooleanField(default=False, verbose_name=_('آیا این پزشک عضو تیم‌پزشکی است؟'))
    is_international = models.BooleanField(default=False, verbose_name=_('آیا این پزشک بین‌الملل است؟'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('پزشک')
        verbose_name_plural = _('پزشکان')

    def __str__(self):
        return f'{self.get_full_name()} - {self.skill_title.title}'

    def get_full_name(self):
        return f'{self.user.firstname()} {self.user.lastname()}'
    get_full_name.short_description = _('نام پزشک')


class TitleSkillModel(models.Model):
    title = TranslatedField(models.CharField(max_length=255, verbose_name=_('عنوان تخصص')))

    class Meta:
        ordering = ['-id']
        verbose_name = _('عنوان تخصص')
        verbose_name_plural = _('عنوان تخصص‌ها')

    def __str__(self):
        return self.title


class DegreeModel(models.Model):
    title = TranslatedField(models.CharField(max_length=255, verbose_name=_('نوع مدرک')))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نوع مدرک')
        verbose_name_plural = _('نوع مدرک‌ها')

    def __str__(self):
        return self.title


class DoctorWorkTimeModel(models.Model):
    doctor = models.ForeignKey(DoctorModel, on_delete=models.SET_NULL, null=True, verbose_name=_('پزشک'))
    day_from = models.CharField(max_length=15, default='saturday', choices=DAYS, verbose_name=_('از روز'))
    day_to = models.CharField(max_length=15, default='thursday', choices=DAYS, verbose_name=_('تا روز'))
    time_from = models.CharField(max_length=15, choices=TIMES, verbose_name=_('از ساعت'))
    time_to = models.CharField(max_length=15, choices=TIMES, verbose_name=_('تا ساعت'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('زمان کاری پزشک')
        verbose_name_plural = _('زمان‌های کاری پزشکان')
    
    def __str__(self):  
        return self.doctor.get_full_name()


class DoctorVacationModel(models.Model):
    doctor = models.ForeignKey(DoctorModel, on_delete=models.SET_NULL, null=True, verbose_name=_('پزشک'))
    from_date = models.DateField(default=timezone.now, verbose_name=_('از تاریخ'))
    to_date = models.DateField(default=timezone.now, verbose_name=_('تا تاریخ'))
    from_time = models.CharField(max_length=15, default='9:00', choices=TIMES, verbose_name=_('از ساعت'))
    to_time = models.CharField(max_length=15, default='12:00', choices=TIMES, verbose_name=_('تا ساعت'))
    is_accepted = models.BooleanField(default=False, verbose_name=_('آیا تایید شده است؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('زمان مرخصی پزشک')
        verbose_name_plural = _('زمان‌های مرخصی پزشکان')
    
    def __str__(self):  
        return self.doctor.get_full_name()

