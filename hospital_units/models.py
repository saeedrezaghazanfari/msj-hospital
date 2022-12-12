from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from extentions.utils import (
    units_image_path, 
    units_map_image_path, 
    get_expriment_code, 
    expriment_result_image_path
)
from hospital_auth.models import User


class UnitModel(models.Model):
    CATEGORY_UNITS = (
        ('technical', _('فنی')), 
        ('hopitalization', _('بستری')), 
        ('clinic', _('کلینیک')), 
        ('paraclinic', _('پاراکلینیک')), 
        ('ipd', _('IPD')), 
        ('official', _('اداری')),
        ('ctscan', _('تصویربرداری-سی تی اسکن')),
        ('radiography_simple', _('تصویربرداری-رادیوگرافی ساده')),
        ('radiography_special', _('تصویربرداری-رادیوگرافی تخصصی')),
        ('mamography', _('تصویربرداری-ماموگرافی')),
        ('sonography', _('تصویربرداری-سونوگرافی')),
    )
    category = models.CharField(max_length=255, choices=CATEGORY_UNITS, verbose_name=_('دسته بندی'))
    have_appointment = models.BooleanField(default=False, verbose_name=_('امکان نوبت دهی آنلاین دارد؟'))
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    inside = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('داخلی'))
    phase = models.IntegerField(verbose_name=_('فاز'))
    floor = models.IntegerField(verbose_name=_('طبقه'))
    image_map = models.ImageField(upload_to=units_map_image_path, blank=True, null=True, verbose_name=_('مکان روی نقشه'))
    manager = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('مسیول'))
    manager_phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('شماره مسیول'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('ایمیل'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('بخش')
        verbose_name_plural = _('بخش ها')

    def __str__(self):
        return self.title


class ExprimentResultModel(models.Model):
    TYPE_EX = (
        ('expriment', _('آزمایش')), 
        ('ctscan', _('تصویربرداری-سی تی اسکن')),
        ('radiography_simple', _('تصویربرداری-رادیوگرافی ساده')),
        ('radiography_special', _('تصویربرداری-رادیوگرافی تخصصی')),
        ('mamography', _('تصویربرداری-ماموگرافی')),
        ('sonography', _('تصویربرداری-سونوگرافی')),
    )
    type = models.CharField(max_length=20, choices=TYPE_EX, verbose_name=_('نوع نتیجه'))
    code = models.CharField(max_length=20, unique=True, default=get_expriment_code, verbose_name=_('کد پیگیری'))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('بیمار'))
    unit = models.ForeignKey(to=UnitModel, on_delete=models.CASCADE, verbose_name=_('بخش'))
    is_show_send_sms = models.BooleanField(default=False, verbose_name=_('بعد از ذخیره کردن آیا نمایش داده شود و پیامک به کاربر ارسال شود؟'))
    title = models.CharField(max_length=255, verbose_name=_('عنوان آزمایش'))
    result = models.CharField(max_length=255, verbose_name=_('جواب آزمایش'))
    image = models.ImageField(upload_to=expriment_result_image_path, verbose_name=_('تصویر آزمایش'))
    date = models.DateTimeField(default=timezone.now, verbose_name=_('زمان ثبت نتیجه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نتیجه آزمایش و تصویربرداری')
        verbose_name_plural = _('نتیجه آزمایش ها و تصویربرداری ها')

    def __str__(self):
        return self.code