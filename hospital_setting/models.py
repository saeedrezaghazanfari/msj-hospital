from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
# from hospital_auth.models import User
from Extentions.utils import (
    costs_image_path, 
    facility_image_path,
    gallery_image_path,
    home_gallery_image_path,
    certificate_image_path,
)


class SettingSDQuerySet(models.QuerySet):
    def delete(self): # delete with queryset
        return self.update(is_deleted=True, deleted_at=timezone.now())

class SettingSDManager(models.Manager):
    def get_queryset(self):
        return SettingSDQuerySet(self.model, self._db).filter(
            Q(is_deleted=False) | Q(is_deleted__isnull=True)
        )

class SettingSDModel(models.Model):
    is_deleted = models.BooleanField(blank=True, null=True, editable=False)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        abstract = True

    objects = SettingSDManager()

    def delete(self, using=None, keep_parents=False): # delete with instance
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()



class SettingModel(models.Model):
    x_scale = models.FloatField(blank=True, null=True, verbose_name=_('مقیاس ایکس'))
    y_scale = models.FloatField(blank=True, null=True, verbose_name=_('مقیاس ایگرگ'))
    marker_text = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('متن شما روی نقشه'))
    address = models.CharField(max_length=255, verbose_name=_('آدرس'))
    email = models.EmailField(max_length=255, verbose_name=_('ایمیل'))
    phone = models.CharField(max_length=255, verbose_name=_('تلفن'))
    from_to = models.CharField(max_length=200, verbose_name=_('زمان گشایش'))
    history = models.TextField(verbose_name=_('تاریخچه'))
    linkedin = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('لینکدین'))
    facebook = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('فیسبوک'))
    twitter = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('توییتر'))
    instagram = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('اینستاگرام'))
    whatsapp = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('واتساپ'))
    bank_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('نام بانک'))
    bank_account_owner = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('نام صاحب حساب'))
    bank_account_cardnum = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('شماره کارت'))
    bank_account_num = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('شماره حساب'))
    bank_account_shabanum = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('شماره شبا'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('‌تنظیمات')
        verbose_name_plural = _('‌تنظیمات')

    def __str__(self):
        return str(_('شما حتما باید یک مقدار در این جدول ذخیره کنید.'))


class CostModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    image = models.ImageField(upload_to=costs_image_path, verbose_name=_('تصویر'))
    year = models.PositiveIntegerField(verbose_name=_('سال'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('ارزش بیمارستان')
        verbose_name_plural = _('ارزش های بیمارستان')

    def __str__(self):
        return self.title


class HospitalPoliticModel(SettingSDModel):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))

    class Meta:
        default_manager_name = 'objects'
        ordering = ['-id']
        verbose_name = _('سیاست بیمارستان')
        verbose_name_plural = _('سیاست های بیمارستان')

    def __str__(self):
        return self.title

class HospitalPoliticRECYCLE(HospitalPoliticModel):
    deleted = models.Manager()
    class Meta:
        proxy = True
        ordering = ['-id']
        verbose_name = _('سیاست بیمارستان - بازیابی')
        verbose_name_plural = _('سیاست های بیمارستان - بازیابی')


class HospitalFacilityModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    image = models.ImageField(upload_to=facility_image_path, verbose_name=_('تصویر'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('امکانات بیمارستان')
        verbose_name_plural = _('امکانات های بیمارستان')

    def __str__(self):
        return self.title


class FAQModel(models.Model):
    question = models.TextField(verbose_name=_('پرسش'))
    answer = models.TextField(verbose_name=_('پاسخ'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('سوال پر تکرار')
        verbose_name_plural = _('سوالات پر تکرار')

    def __str__(self):
        return self.question


class NewsLetterModel(models.Model):
    email = models.EmailField(max_length=255, verbose_name=_('ایمیل'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('خبرنامه')
        verbose_name_plural = _('خبرنامه')

    def __str__(self):
        return self.email


class InsuranceModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('نام بیمه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('بیمه طرف قرارداد')
        verbose_name_plural = _('بیمه های طرف قرارداد')

    def __str__(self):
        return self.title


class HospitalGalleryModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    items = models.ManyToManyField('HospitalGalleryItemModel', verbose_name=_('آیتم/آیتم ها'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گالری بیمارستان')
        verbose_name_plural = _('گالری های بیمارستان')

    def __str__(self):
        return self.title


class HospitalGalleryItemModel(models.Model):
    FILE_TYPES = (('video', _('ویدیو')), ('image', _('تصویر')))
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, verbose_name=_('نوع فایل'))
    file = models.FileField(upload_to=gallery_image_path, verbose_name=_('فایل'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('آیتم گالری')
        verbose_name_plural = _('آیتم های گالری')

    def __str__(self):
        return self.title


class ReportModel(models.Model):
    time_bound = models.CharField(max_length=100, verbose_name=_('مدت عملکرد'))
    description = models.TextField(verbose_name=_('توضیحات'))
    image = models.ImageField(upload_to=gallery_image_path, verbose_name=_('تصویر'))
    video = models.FileField(upload_to=gallery_image_path, verbose_name=_('ویدیو'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گزارش بیمارستان')
        verbose_name_plural = _('گزارش های بیمارستان')

    def __str__(self):
        return self.time_bound


class PriceModel(models.Model):
    title = models.CharField(max_length=400, verbose_name=_('عنوان'))
    price = models.PositiveBigIntegerField(verbose_name=_('مبلغ'))
    type_service = models.CharField(max_length=500, verbose_name=_('نوع خدمت'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تعرفه')
        verbose_name_plural = _('تعرفه ها')

    def __str__(self):
        return self.title


class ResultModel(models.Model):
    title = models.CharField(max_length=500, verbose_name=_('عنوان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('دستاورد بیمارستان')
        verbose_name_plural = _('دستاورد های بیمارستان')

    def __str__(self):
        return self.title


class HomeGalleryModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('عنوان'))
    subtitle = models.CharField(max_length=255, verbose_name=_('متن'))
    image = models.ImageField(upload_to=home_gallery_image_path, verbose_name=_('تصویر'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('آیتم گالری صفحه ی خانه')
        verbose_name_plural = _('آیتم های گالری صفحه ی خانه')

    def __str__(self):
        return self.title


class CertificateModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('عنوان'))
    description = models.TextField(verbose_name=_('توضیحات'))
    image = models.ImageField(upload_to=certificate_image_path, verbose_name=_('تصویر'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گواهینامه')
        verbose_name_plural = _('گواهینامه ها')

    def __str__(self):
        return self.title

