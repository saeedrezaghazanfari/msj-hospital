from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from extentions.utils import (
    units_image_path, 
    units_map_image_path, 
    get_expriment_code, 
    expriment_result_image_path,
    code_patient_turn
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


class AppointmentTimeModel(models.Model):
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
        ('6-7', '6-7'),
        ('7-8', '7-8'),
        ('8-9', '8-9'),
        ('9-10', '9-10'),
        ('10-11', '10-11'),
        ('11-12', '11-12'),
        ('12-13', '12-13'),
        ('13-14', '13-14'),
        ('14-15', '14-15'),
        ('15-16', '15-16'),
        ('16-17', '16-17'),
        ('17-18', '17-18'),
        ('18-19', '18-19'),
        ('19-20', '19-20'),
        ('20-21', '20-21'),
        ('21-22', '21-22'),
        ('22-23', '22-23'),
        ('23-24', '23-24'),
    )
    unit = models.ForeignKey(to=UnitModel, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('بخش'), help_text=_('اگر مقداری به این قسمت داده نشود در اینصورت بخش پزشکان انتخاب میشود.'))
    doctor = models.ForeignKey(to='hospital_doctor.DoctorModel', on_delete=models.CASCADE, verbose_name=_('پزشک'))
    date = models.DateField(default=timezone.now, verbose_name=_('تاریخ روز'))
    day = models.CharField(max_length=15, choices=DAYS, verbose_name=_('روز'))
    time = models.CharField(max_length=15, choices=TIMES, verbose_name=_('بازه ی زمانی'))
    price = models.ForeignKey(to='hospital_setting.PriceAppointmentModel', on_delete=models.CASCADE, verbose_name=_('تعرفه'))
    capacity = models.PositiveIntegerField(verbose_name=_('ظرفیت کل'))
    reserved = models.PositiveIntegerField(verbose_name=_('تعداد رزرو شده'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('زمان نوبتدهی')
        verbose_name_plural = _('زمان های نوبتدهی')

    def __str__(self):
        return self.doctor


class PatientTurnModel(models.Model):
    GENDER_USER = (('male', _('مرد')), ('female', _('زن')))

    code = models.CharField(max_length=15, default=code_patient_turn, verbose_name=_('کد پیگیری'))
    appointment = models.ForeignKey(to=AppointmentTimeModel, on_delete=models.CASCADE, verbose_name=_('زمان مشاوره'))
    reserver = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('رزرو کننده'))
    full_name = models.CharField(max_length=50, verbose_name=_('نام و نام خانوادگی بیمار'))
    national_code = models.CharField(max_length=10, unique=True, verbose_name=_('کدملی بیمار'))
    phone = models.CharField(max_length=20, default=0, verbose_name=_('شماره تلفن بیمار'))
    age = models.PositiveIntegerField(verbose_name=_('سن بیمار'))
    gender = models.CharField(choices=GENDER_USER, max_length=7, verbose_name=_('جنسیت بیمار'))
    insurance = models.ForeignKey(to='hospital_setting.InsuranceModel', on_delete=models.CASCADE, verbose_name=_('بیمه'))
    insurance_code = models.PositiveBigIntegerField(verbose_name=_('کد بیمه'))
    price = models.PositiveBigIntegerField(verbose_name=_('مبلغ قابل پرداخت'))
    prescription_code = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('کد نسخه ی پزشک دیگر'))
    turn = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('نوبت فیزیکی بیمار'))
    is_paid = models.BooleanField(default=False, verbose_name=_('پرداخت شده؟'))
    is_canceled = models.BooleanField(default=False, verbose_name=_('آیا از سمت بیمار کنسل شده است؟'))
    is_canceled = models.BooleanField(default=False, verbose_name=_('آیا از مبلغ کنسل شدن به بیمار واریز شده است؟'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('نوبت بیمار')
        verbose_name_plural = _('نوبت بیماران')

    def __str__(self):
        return self.full_name


class OnlinePaymentModel(models.Model):
    payer = models.ForeignKey(to=PatientTurnModel, on_delete=models.CASCADE, verbose_name=_('پرداخت کننده'))
    price = models.PositiveBigIntegerField(verbose_name=_('مبلغ پرداختی'))
    is_success = models.BooleanField(default=False, verbose_name=_('آیا تراکنش موفقیت آمیز بوده است؟'))
    code = models.CharField(max_length=50, verbose_name=_('شماره پرداخت'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('پرداخت اینترنتی')
        verbose_name_plural = _('پرداخت های اینترنتی')

    def __str__(self):
        return self.payer