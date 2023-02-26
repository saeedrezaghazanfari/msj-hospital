import uuid
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from hospital_auth.models import User
from extentions.utils import (
    jalali_convertor, 
    ipd_doc_image_path,
    get_random_code,
    get_patient_tracking_code
)


class IPDModel(models.Model):
    GENDER_USER = (('male', _('مرد')), ('female', _('زن')))

    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    code = models.IntegerField(null=True, default=get_patient_tracking_code, verbose_name=_('کد'))
    username = models.CharField(max_length=10, verbose_name=_('شماره پاسپورت / کدملی'))
    first_name = models.CharField(max_length=100, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))
    phone = models.CharField(max_length=20, default=0, verbose_name=_('شماره تلفن'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('ایمیل'))
    gender = models.CharField(choices=GENDER_USER, default='male', max_length=7, verbose_name=_('جنسیت'))
    age = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('سن'))
    description = RichTextField(verbose_name=_('شرح بیماری'))
    document = models.FileField(upload_to=ipd_doc_image_path, null=True, blank=True, verbose_name=_('مستندات'))
    country = models.CharField(max_length=100, verbose_name=_('کشور'))
    state = models.CharField(max_length=100, null=True, verbose_name=_('استان'))
    city = models.CharField(max_length=100, null=True, verbose_name=_('شهر'))
    created = models.DateTimeField(auto_now_add=True)
    answer = RichTextField(blank=True, null=True, verbose_name=_('پاسخ'))
    doctor_answerer = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('پزشک پاسخگو'))
    is_answered = models.BooleanField(default=False, verbose_name=_('آیا جواب داده شده است؟'))

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    get_full_name.short_description = _('نام و نام خانوادگی')

    def j_created(self):
        return jalali_convertor(time=self.created, output='j_date')
    j_created.short_description = _('تاریخ ارسال درخواست')

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = _('بیمار بین الملل')
        verbose_name_plural = _('بیماران بین الملل')


class IPDCodeModel(models.Model):
    phone = models.CharField(max_length=30, verbose_name=_('شماره تلفن'))
    code = models.IntegerField(default=get_random_code, unique=True, verbose_name=_('کد'))
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
        verbose_name = _('کد احراز هویت ipd')
        verbose_name_plural = _('کدهای احراز هویت ipd')


# signals
@receiver(post_save, sender=IPDCodeModel)
def set_expire_date(sender, instance, created, **kwargs):
    if created:
        instance.expire_date = timezone.now() + timezone.timedelta(seconds=90)
        instance.expire_mission = timezone.now() + timezone.timedelta(minutes=30)
        instance.save()
