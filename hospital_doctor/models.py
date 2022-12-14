from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from hospital_auth.models import User
from hospital_units.models import UnitModel
from extentions.utils import profile_image_path, DAYS, TIMES


class DoctorModel(models.Model):
    medical_code = models.BigIntegerField(verbose_name=_('کد نظام پزشکی'))
    skill_title = models.ForeignKey('TitleSkillModel', on_delete=models.SET_NULL, null=True, verbose_name=_('عنوان تخصص'))
    user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('کاربر'))
    units = models.ManyToManyField(to=UnitModel, verbose_name=_('بخش ها'))
    position = models.TextField(max_length=500, null=True, blank=True, verbose_name=_('موقعیت'))
    degree = models.ForeignKey('DegreeModel', on_delete=models.SET_NULL, null=True, verbose_name=_('نوع مدرک'))
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('بیوگرافی'))
    is_intenational = models.BooleanField(default=False, verbose_name=_('آیا این پزشک بین الملل است؟'))
    is_medicalteam = models.BooleanField(default=False, verbose_name=_('آیا این پزشک عضو تیم پزشکی است؟'))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال/غیرفعال'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('پزشک')
        verbose_name_plural = _('پزشکان')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    get_full_name.short_description = _('نام پزشک')


class TitleSkillModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('عنوان تخصص'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('عنوان تخصص')
        verbose_name_plural = _('عناوین تخصص‌ها')

    def __str__(self):
        return self.title


class DegreeModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نوع مدرک'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نوع مدرک')
        verbose_name_plural = _('نوع مدرک ها')

    def __str__(self):
        return self.title


class DoctorWorkTimeModel(models.Model):
    doctor = models.ForeignKey(DoctorModel, on_delete=models.SET_NULL, null=True, verbose_name=_('پزشک'))
    day = models.CharField(max_length=15, choices=DAYS, verbose_name=_('روز'))
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
    from_time = models.DateField(default=timezone.now, verbose_name=_('از تاریخ'))
    to_time = models.DateField(default=timezone.now, verbose_name=_('تا تاریخ'))
    is_accepted = models.BooleanField(default=False, verbose_name=_('آیا تایید شده است؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('زمان مرخصی پزشک')
        verbose_name_plural = _('زمان‌های مرخصی پزشکان')
    
    def __str__(self):  
        return self.doctor.get_full_name()


class InternationalPatientModel(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('بیمار بین الملل')
        verbose_name_plural = _('بیماران بین الملل')
    
    def __str__(self):  
        return f'{self.first_name} {self.last_name}'


class FamousPatientModel(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))
    profile = models.ImageField(upload_to=profile_image_path, verbose_name=_('تصویر'))
    desc = models.TextField(verbose_name=_('متن'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('چهره سرشناس مراجعه کننده')
        verbose_name_plural = _('چهره های سرشناس مراجعه کننده')
    
    def __str__(self):  
        return f'{self.first_name} {self.last_name}'