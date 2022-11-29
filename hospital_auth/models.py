from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from Extentions.utils import get_user_code, user_image_path, jalali_convertor, get_random_code


class User(AbstractUser):
    GENDER_USER = (('male', _('مرد')), ('female', _('زن')))
    username = models.CharField(max_length=12, unique=True, default=get_user_code, editable=False, verbose_name=_('کد کاربری'))
    phone = models.BigIntegerField(blank=True, null=True, verbose_name=_('شماره تلفن'))
    profile = models.ImageField(upload_to=user_image_path, null=True, blank=True, verbose_name=_('پروفایل'))
    wallet_balance = models.FloatField(default=0, verbose_name=_('موجودی کیف پول'))
    is_send_sms = models.BooleanField(default=False, verbose_name=_('آیا پیامک های پزشکی ارسال شود؟'))
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    get_full_name.short_description = _('نام و نام خانوادگی')

    class Meta:
        ordering = ['-id']
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')


class LoginCodeModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    code = models.IntegerField(default=get_random_code, verbose_name=_('کد'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ تولید کد'))
    expire_date = models.DateTimeField(blank=True, null=True, verbose_name=_('تاریخ انقضای کد'), help_text=_('این فیلد لازم نیست پر شود. بعد از ثبت رکورد بصورت اتوماتیک ثبت میشود.'))
    is_use = models.BooleanField(default=False, verbose_name=_('استفاده شده؟'))

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
        verbose_name = _('کد ورود به حساب کاربری')
        verbose_name_plural = _('کدهای ورود به حساب های کاربری')



# signals
@receiver(post_save, sender=LoginCodeModel)
def set_expire_date(sender, instance, created, **kwargs):
    if created:
        instance.expire_date = timezone.now() + timezone.timedelta(minutes=3)
        instance.save()