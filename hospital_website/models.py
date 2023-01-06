from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from extentions.utils import get_random_code, jalali_convertor


class LoginCodePatientModel(models.Model):
    phone = models.CharField(max_length=30, verbose_name=_('شماره تلفن'))
    code = models.IntegerField(default=get_random_code, verbose_name=_('کد'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ تولید کد'))
    expire_date = models.DateTimeField(blank=True, null=True, verbose_name=_('تاریخ انقضای کد'))
    is_use = models.BooleanField(default=False, verbose_name=_('استفاده شده؟'))
    expire_mission = models.DateTimeField(blank=True, null=True, verbose_name=_('تاریخ انقضای عملیات'))

    def __str__(self):
        return str(self.id)

    def j_date(self):
        return jalali_convertor(time=self.date, number=True)
    j_date.short_description = _('تاریخ تولید کد')

    def j_expire(self):
        return jalali_convertor(time=self.expire_date, number=True)
    j_expire.short_description = _('تاریخ انقضای کد')

    class Meta: 
        ordering = ['-id']
        verbose_name = _('کد ارسال شده به شماره بیمار')
        verbose_name_plural = _('کدهای ارسال شده به شماره بیماران ')


# signals
@receiver(post_save, sender=LoginCodePatientModel)
def set_expire_date(sender, instance, created, **kwargs):
    if created:
        instance.expire_date = timezone.now() + timezone.timedelta(seconds=90)
        instance.expire_mission = timezone.now() + timezone.timedelta(minutes=15)
        instance.save()