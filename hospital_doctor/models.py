from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from hospital_auth.models import User
from hospital_units.models import ClinicModel


class DoctorModel(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('بیوگرافی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('پزشک')
        verbose_name_plural = _('پزشک ها')

    def __str__(self):
        return str(self.user.get_full_name())

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    get_full_name.short_description = _('نام پزشک')


class DoctorSkillModel(models.Model):
    medical_code = models.IntegerField(verbose_name=_('کد نظام پزشکی'))
    skill_title = models.ForeignKey('TitleSkillModel', on_delete=models.CASCADE, verbose_name=_('عنوان تخصص'))
    doctor = models.ForeignKey(to=DoctorModel, on_delete=models.CASCADE, verbose_name=_('پزشک'))
    clinic = models.ForeignKey(to=ClinicModel, on_delete=models.CASCADE, verbose_name=_('کلینیک'))
    position = models.TextField(max_length=500, verbose_name=_('موقعیت'))
    description = models.TextField(blank=True, null=True, verbose_name=_('توضیحات'))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال/غیرفعال'))


    class Meta:
        ordering = ['-id']
        verbose_name = _('عنوان تخصص')
        verbose_name_plural = _('عناوین تخصص‌ها')

    def __str__(self):
        return self.title


class TitleSkillModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('عنوان تخصص'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('عنوان تخصص')
        verbose_name_plural = _('عناوین تخصص‌ها')

    def __str__(self):
        return self.title


class DoctorWorkTimeModel(models.Model):
    DAYS = (
        ('saturday', _('شنبه')),
        ('sunday', _('یک شنبه')),
        ('monday', _('دو شنبه')),
        ('tuesday', _('سه شنبه')),
        ('wednesday', _('چهار شنبه')),
        ('thursday', _('پنج شنبه')),
        ('friday', _('جمعه')),
    )
    TIMES = (
        ('6-8', '6-8'),
        ('8-10', '8-10'),
        ('10-12', '10-12'),
        ('12-14', '12-14'),
        ('14-16', '14-16'),
        ('16-18', '16-18'),
        ('18-20', '18-20'),
        ('20-22', '20-22'),
    )
    doctor = models.ForeignKey(DoctorSkillModel, on_delete=models.CASCADE, verbose_name=_('پزشک'))
    day = models.CharField(max_length=15, choices=DAYS, verbose_name=_('روز'))
    time = models.CharField(max_length=15, choices=TIMES, verbose_name=_('زمان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('زمان کاری پزشک')
        verbose_name_plural = _('زمان‌های کاری پزشکان')
    
    def __str__(self):  
        return self.doctor.doctor.get_full_name()


class DoctorVacationModel(models.Model):
    doctor = models.ForeignKey(DoctorSkillModel, on_delete=models.CASCADE, verbose_name=_('پزشک'))
    from_time = models.DateField(default=timezone.now, verbose_name=_('از تاریخ'))
    to_time = models.DateField(default=timezone.now, verbose_name=_('تا تاریخ'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('زمان مرخصی پزشک')
        verbose_name_plural = _('زمان‌های مرخصی پزشکان')
    
    def __str__(self):  
        return self.doctor.doctor.get_full_name()