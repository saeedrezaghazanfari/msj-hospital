from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField
from hospital_doctor.models import DegreeModel
from hospital_auth.models import User
from extentions.utils import (
    costs_image_path, 
    facility_image_path,
    gallery_image_path,
    home_gallery_image_path,
    certificate_image_path,
    insurance_image_path,
    report_image_path,
    news_letter_image_path,
    ancient_image_path
)


class SettingModel(models.Model):
    x_scale = models.FloatField(blank=True, null=True, verbose_name=_('مقیاس ایکس'))
    y_scale = models.FloatField(blank=True, null=True, verbose_name=_('مقیاس ایگرگ'))
    marker_text = TranslatedField(models.CharField(max_length=50, blank=True, null=True, verbose_name=_('متن شما روی نقشه')))
    address = TranslatedField(models.CharField(max_length=255, verbose_name=_('آدرس')))
    email = models.EmailField(max_length=255, verbose_name=_('ایمیل'))
    phone = models.CharField(max_length=255, verbose_name=_('تلفن'))
    facs = models.CharField(max_length=255, verbose_name=_('فکس'))
    from_to = TranslatedField(models.CharField(max_length=200, verbose_name=_('زمان گشایش')))
    history = TranslatedField(models.TextField(verbose_name=_('تاریخچه')))
    aparat = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('آپارات'))
    linkedin = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('لینکدین'))
    facebook = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('فیسبوک'))
    twitter = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('توییتر'))
    instagram = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('اینستاگرام'))
    whatsapp = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('واتساپ'))
    bank_name = TranslatedField(models.CharField(max_length=100, blank=True, null=True, verbose_name=_('نام بانک')))
    bank_account_owner = TranslatedField(models.CharField(max_length=100, blank=True, null=True, verbose_name=_('نام صاحب حساب')))
    bank_account_cardnum = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('شماره کارت'))
    bank_account_num = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('شماره حساب'))
    bank_account_shabanum = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('شماره شبا'))
    have_signup_page = models.BooleanField(default=False, verbose_name=_('صفحه ثبتنام کاربران نمایش داده شود؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('‌تنظیمات')
        verbose_name_plural = _('‌تنظیمات')

    def __str__(self):
        return str(_('شما حتما باید یک مقدار در این جدول ذخیره کنید.'))


class CostModel(models.Model):
    title = TranslatedField(models.CharField(max_length=100, verbose_name=_('عنوان')))
    image = models.ImageField(upload_to=costs_image_path, verbose_name=_('تصویر'))
    year = models.PositiveIntegerField(verbose_name=_('سال'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('ارزش بیمارستان')
        verbose_name_plural = _('ارزش های بیمارستان')

    def __str__(self):
        return self.title


class HospitalPoliticModel(models.Model):
    title = TranslatedField(models.CharField(max_length=100, verbose_name=_('عنوان')))

    class Meta:
        ordering = ['-id']
        verbose_name = _('سیاست بیمارستان')
        verbose_name_plural = _('سیاست های بیمارستان')

    def __str__(self):
        return self.title


class HospitalFacilityModel(models.Model):
    title = TranslatedField(models.CharField(max_length=100, verbose_name=_('عنوان')))
    image = models.ImageField(upload_to=facility_image_path, verbose_name=_('تصویر'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('امکانات بیمارستان')
        verbose_name_plural = _('امکانات های بیمارستان')

    def __str__(self):
        return self.title


class FAQModel(models.Model):
    question = TranslatedField(models.TextField(verbose_name=_('پرسش')))
    answer = TranslatedField(models.TextField(verbose_name=_('پاسخ')))

    class Meta:
        ordering = ['-id']
        verbose_name = _('سوال پر تکرار')
        verbose_name_plural = _('سوالات پر تکرار')

    def __str__(self):
        return self.question


class NewsLetterEmailsModel(models.Model):
    email = models.EmailField(max_length=255, verbose_name=_('ایمیل'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('ایمیل خبرنامه')
        verbose_name_plural = _('ایمیل های خبرنامه')

    def __str__(self):
        return self.email


class NewsLetterModel(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('نویسنده'))
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    image = models.ImageField(upload_to=news_letter_image_path, verbose_name=_('تصویر'))
    read_time = models.PositiveIntegerField(default=0, verbose_name=_('زمان خواندن'))
    desc = models.TextField(verbose_name=_('متن'))
    is_send = models.BooleanField(default=False, verbose_name=_('آیا ایمیل شوند؟'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('خبرنامه')
        verbose_name_plural = _('خبرنامه')

    def __str__(self):
        return self.title


class InsuranceModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('نام بیمه'))
    img = models.ImageField(upload_to=insurance_image_path, verbose_name=_('تصویر'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('بیمه طرف قرارداد')
        verbose_name_plural = _('بیمه های طرف قرارداد')

    def __str__(self):
        return self.title


class HospitalGalleryModel(models.Model):
    title = TranslatedField(models.CharField(max_length=100, verbose_name=_('عنوان')))
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
    file = models.ImageField(upload_to=gallery_image_path, blank=True, null=True, verbose_name=_('فایل'), help_text=_('اگر فایل شما تصویر میباشد تصویر مورد نظر را وارد کنید.'))
    file_link = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('لینک فایل'), help_text=_('اگر فایل شما ویدیو میباشد لینک فیلم را وارد کنید.'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('آیتم گالری')
        verbose_name_plural = _('آیتم های گالری')

    def __str__(self):
        return self.title


class ReportModel(models.Model):
    time_bound = models.CharField(max_length=100, verbose_name=_('مدت عملکرد'))
    description = TranslatedField(models.TextField(verbose_name=_('توضیحات')))
    image = models.ImageField(upload_to=report_image_path, blank=True, null=True, verbose_name=_('تصویر'))
    video_link = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('لینک ویدیو'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گزارش عملکرد بیمارستان')
        verbose_name_plural = _('گزارش عملکرد های بیمارستان')

    def __str__(self):
        return self.time_bound


class PriceAppointmentModel(models.Model):
    insurance = models.ForeignKey(to=InsuranceModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('بیمه'))
    degree = models.ForeignKey(to=DegreeModel, on_delete=models.SET_NULL, null=True, verbose_name=_('نوع مدرک'))
    price = models.PositiveBigIntegerField(default=0, verbose_name=_('مبلغ'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تعرفه ی نوبت دهی')
        verbose_name_plural = _('تعرفه ی نوبت دهی ها')

    def __str__(self):
        return f'{self.insurance.title} - {self.degree.title}'


class ResultModel(models.Model):
    title = TranslatedField(models.CharField(max_length=100, verbose_name=_('عنوان')))
    desc = TranslatedField(models.TextField(verbose_name=_('متن')))

    class Meta:
        ordering = ['-id']
        verbose_name = _('دستاورد بیمارستان')
        verbose_name_plural = _('دستاورد های بیمارستان')

    def __str__(self):
        return self.title


class HomeGalleryModel(models.Model):
    title = TranslatedField(models.CharField(max_length=255, verbose_name=_('عنوان')))
    image = models.ImageField(upload_to=home_gallery_image_path, verbose_name=_('تصویر'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('آیتم گالری صفحه ی خانه')
        verbose_name_plural = _('آیتم های گالری صفحه ی خانه')

    def __str__(self):
        return self.title


class CertificateModel(models.Model):
    title = TranslatedField(models.CharField(max_length=255, verbose_name=_('عنوان')))
    description = TranslatedField(models.TextField(verbose_name=_('توضیحات')))
    image = models.ImageField(upload_to=certificate_image_path, verbose_name=_('تصویر'))
    year_certif = models.IntegerField(verbose_name=_('سال اخذ'))
    year_expire = models.IntegerField(verbose_name=_('تاریخ اعتبار'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گواهینامه')
        verbose_name_plural = _('گواهینامه ها')

    def __str__(self):
        return self.title


class ContactInfoModel(models.Model):
    title = TranslatedField(models.CharField(max_length=500, verbose_name=_('عنوان')))
    phones = models.CharField(max_length=100, verbose_name=_('تلفن ها'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('ایمیل'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('اطلاعات تماس')
        verbose_name_plural = _('اطلاعات تماس')

    def __str__(self):
        return self.title


class PriceServiceModel(models.Model):
    title = TranslatedField(models.CharField(max_length=200, verbose_name=_('عنوان')))
    desc = TranslatedField(models.TextField(verbose_name=_('متن')))
    price_special = models.PositiveBigIntegerField(verbose_name=_('مبلغ خصوصی'))
    price_govern = models.PositiveBigIntegerField(verbose_name=_('مبلغ دولتی'))
    diffrence = models.PositiveBigIntegerField(verbose_name=_('تفاوت'))
    year = models.IntegerField(verbose_name=_('سال تعرفه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تعرفه خدمات بیمارستان')
        verbose_name_plural = _('تعرفه خدمات بیمارستان')

    def __str__(self):
        return self.title


class PriceBedModel(models.Model):
    title = TranslatedField(models.CharField(max_length=200, verbose_name=_('عنوان')))
    price_free = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_('مبلغ آزاد'))
    insurance = models.ForeignKey(to=InsuranceModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('بیمه'))
    price_insurance = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_('مبلغ بیمه'))
    year = models.IntegerField(verbose_name=_('سال تعرفه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تعرفه تخت بیمارستان')
        verbose_name_plural = _('تعرفه تخت های بیمارستان')

    def __str__(self):
        return self.title


class PriceSurgrayModel(models.Model):
    title = TranslatedField(models.CharField(max_length=200, verbose_name=_('عنوان')))
    price_free = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_('مبلغ آزاد'))
    insurance = models.ForeignKey(to=InsuranceModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('بیمه'))
    price_insurance = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_('مبلغ بیمه'))
    year = models.IntegerField(verbose_name=_('سال تعرفه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تعرفه عمل جراحی بیمارستان')
        verbose_name_plural = _('تعرفه عمل جراحی های بیمارستان')

    def __str__(self):
        return self.title


class AncientsModel(models.Model):
    title = TranslatedField(models.CharField(max_length=200, verbose_name=_('عنوان')))
    image = models.ImageField(upload_to=ancient_image_path, verbose_name=_('تصویر'))
    full_name = TranslatedField(models.CharField(max_length=255, verbose_name=_('نام پزشک مرحوم')))
    description = TranslatedField(models.TextField(verbose_name=_('متن')))
    gallery = models.ManyToManyField('HospitalGalleryItemModel', verbose_name=_('گالری'))
    video_link = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('لینک ویدیو'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گذشتگان بیمارستان')
        verbose_name_plural = _('گذشتگان بیمارستان')

    def __str__(self):
        return self.full_name


