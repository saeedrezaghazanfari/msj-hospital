import uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField
from hospital_auth.models import PatientModel
from django.utils.translation import get_language
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from hospital_extentions.utils import (
    GENDERS,
    jalali_convertor,
    units_image_path, 
    units_icon_image_path,
    get_experiment_code, 
    experiment_result_image_path,
    code_patient_turn,
    DAYS, TIMES,
    unit_member_image_path,
    managers_image_path,
    get_links_code,
    get_random_code,
)


class UnitModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    subunit = models.ForeignKey(to='SubUnitModel', on_delete=models.SET_NULL, null=True, verbose_name=_('عنوان بخش'))
    title = TranslatedField(models.CharField(max_length=255, blank=True, null=True, verbose_name=_('نام')))
    desc = TranslatedField(RichTextField(verbose_name=_('متن')))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    inside = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('داخلی'))
    address = TranslatedField(models.CharField(max_length=255, verbose_name=_('آدرس')))
    work_times = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('ساعات کاری'))
    manager = TranslatedField(models.CharField(max_length=100, blank=True, null=True, verbose_name=_('مسئول')))
    manager_phone = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('شماره مسئول'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('ایمیل'))
    icon = models.ImageField(upload_to=units_icon_image_path, blank=True, null=True, verbose_name=_('آیکون بخش'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('بخش')
        verbose_name_plural = _('بخش‌ها')

    def category_slug(self):
        return self.subunit.slug

    def __str__(self):
        lang = get_language()
        if lang == 'fa':
            if self.title_fa:
                return f'{self.subunit.title_fa} ({self.title_fa})'
            return f'{self.subunit}'
            
        if lang == 'en':
            if self.title_en:
                return f'{self.subunit.title_en} ({self.title_en})'
            return f'{self.subunit}'

        if lang == 'ar':
            if self.title_ar:
                return f'{self.subunit.title_ar} ({self.title_ar})'
            return f'{self.subunit}'

        if lang == 'ru':
            if self.title_ru:
                return f'{self.subunit.title_ru} ({self.title_ru})'
            return f'{self.subunit}'


class SubUnitModel(models.Model):
    CATEGORY_UNITS = (
        ('medical', _('درمانی')), 
        ('paraclinic', _('پاراکلینیک')), 
        ('official', _('غیردرمانی')),
    )
    slug = models.SlugField(default=get_links_code, unique=True, verbose_name=_('نمایش در url'))
    category = models.CharField(max_length=255, null=True, choices=CATEGORY_UNITS, verbose_name=_('دسته بندی بخش'))
    title = TranslatedField(models.CharField(max_length=255, verbose_name=_('نام')))
    have_2_box = models.BooleanField(default=False, verbose_name=_('آیا دو قسمتی است؟'), help_text=_('در بخش نوبت‌دهی اینترنتی باعث میشود که کاربر به ۲ طریق مختلف رزرو اینترنتی انجام دهد.'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('عنوان بخش')
        verbose_name_plural = _('عناوین بخش')

    def __str__(self):
        return f'{self.title}'


class ManagersModel(models.Model):
    USER_TYPE = (('hm', _('هیات مدیره')), ('magm', _('مدیرعامل و گروه مدیریت')))

    label = models.CharField(max_length=255, choices=USER_TYPE, verbose_name=_('دسته‌بندی نمایش'))
    first_name = TranslatedField(models.CharField(max_length=100, verbose_name=_('نام')))
    last_name = TranslatedField(models.CharField(max_length=100, verbose_name=_('نام‌خانوادگی')))
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('شماره تلفن'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('ایمیل'))
    gender = models.CharField(choices=GENDERS, default='male', max_length=7, verbose_name=_('جنسیت'))
    job = TranslatedField(models.CharField(max_length=255, verbose_name=_('سمت')))
    profile = models.ImageField(upload_to=managers_image_path, null=True, blank=True, verbose_name=_('پروفایل'))
    linkedin = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('لینکدین'))
    facebook = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('فیسبوک'))
    twitter = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('توییتر'))
    instagram = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('اینستاگرام'))
    whatsapp = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('واتساپ'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('مدیریت بیمارستان')
        verbose_name_plural = _('مدیریت بیمارستان')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    get_full_name.short_description = _('نام و نام‌خانوادگی')

    def __str__(self):
        return self.get_full_name()


class UnitMemberModel(models.Model):
    unit = models.ForeignKey(UnitModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بخش'))
    first_name = TranslatedField(models.CharField(max_length=100, verbose_name=_('نام')))
    last_name = TranslatedField(models.CharField(max_length=100, verbose_name=_('نام‌خانوادگی')))
    phone = models.CharField(max_length=100, default=0, verbose_name=_('شماره تلفن'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('ایمیل'))
    gender = models.CharField(choices=GENDERS, default='male', max_length=7, verbose_name=_('جنسیت'))
    job = TranslatedField(models.CharField(max_length=255, verbose_name=_('سمت')))
    profile = models.ImageField(upload_to=unit_member_image_path, null=True, blank=True, verbose_name=_('پروفایل'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('عضو بخش')
        verbose_name_plural = _('اعضای بخش‌ها')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    get_full_name.short_description = _('نام و نام‌خانوادگی')

    def __str__(self):
        return self.get_full_name()


class ExprimentResultModel(models.Model):
    code = models.CharField(max_length=20, unique=True, default=get_experiment_code, verbose_name=_('کد پیگیری'))
    patient = models.ForeignKey(to=PatientModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بیمار'))
    unit = models.ForeignKey(to=UnitModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بخش'))
    title = models.CharField(max_length=255, verbose_name=_('عنوان آزمایش'))
    result = RichTextField(blank=True, null=True, verbose_name=_('جواب آزمایش'))
    image = models.ImageField(upload_to=experiment_result_image_path, blank=True, null=True, verbose_name=_('تصویر آزمایش'))
    date = models.DateField(blank=True, null=True, verbose_name=_('زمان ثبت نتیجه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نتیجه آزمایش و تصویربرداری')
        verbose_name_plural = _('نتیجه آزمایش‌ها و تصویربرداری‌ها')

    def __str__(self):
        return self.code


class AppointmentTimeModel(models.Model):
    STATUS = (('invac', _('مرخصی پزشک')), ('normal', _('معمولی')), )
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    unit = models.ForeignKey(to=UnitModel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('بخش'), help_text=_('اگر مقداری به این قسمت داده نشود در اینصورت بخش پزشکان انتخاب میشود.'))
    doctor = models.ForeignKey(to='hospital_doctor.DoctorModel', on_delete=models.SET_NULL, null=True, verbose_name=_('پزشک'))
    date = models.DateField(default=timezone.now, verbose_name=_('تاریخ روز'))
    day = models.CharField(max_length=15, choices=DAYS, verbose_name=_('روز'))
    time_from = models.CharField(max_length=15, choices=TIMES, verbose_name=_('از ساعت'))
    time_to = models.CharField(max_length=15, choices=TIMES, verbose_name=_('تا ساعت'))
    insurances = models.ManyToManyField(to='hospital_setting.InsuranceModel', verbose_name=_('بیمه‌ها'))
    capacity = models.IntegerField(verbose_name=_('ظرفیت کل'))
    reserved = models.PositiveIntegerField(default=0, verbose_name=_('تعداد رزرو شده'))
    status = models.CharField(max_length=15, default='normal', choices=STATUS, verbose_name=_('وضعیت'))
    tip = models.ForeignKey(to='AppointmentTipModel', on_delete=models.SET_NULL, null=True, verbose_name=_('نکات نوبت‌دهی'))
    tip_sms = models.ForeignKey(to='AppointmentTipSMSModel', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('نکات نوبت‌دهی در پیامک'))

    class Meta:
        ordering = ['date']
        verbose_name = _('زمان نوبت‌دهی')
        verbose_name_plural = _('زمان‌های نوبت‌دهی')

    def j_date(self):
        return jalali_convertor(time=self.date, number=True)
    j_date.short_description = _('تاریخ روز')

    def __str__(self):
        return f'{self.doctor.user.firstname()} {self.doctor.user.lastname()} - {self.date}'


class AppointmentTipModel(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('عنوان'))
    tips = RichTextField(verbose_name=_('نکات'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نکات نوبت‌دهی')
        verbose_name_plural = _('نکات نوبت‌دهی')

    def __str__(self):
        return self.title


class AppointmentTipSMSModel(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('عنوان'))
    tips = models.TextField(verbose_name=_('نکات'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نکات نوبت‌دهی در پیامک')
        verbose_name_plural = _('نکات نوبت‌دهی در پیامک')

    def __str__(self):
        return self.title


class PatientTurnModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    code = models.CharField(max_length=15, default=code_patient_turn, verbose_name=_('کد پیگیری نوبت'))
    patient = models.ForeignKey(to=PatientModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بیمار'))
    appointment = models.ForeignKey(to=AppointmentTimeModel, on_delete=models.SET_NULL, null=True, verbose_name=_('زمان مشاوره'))
    insurance = models.ForeignKey(to='hospital_setting.InsuranceModel', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('بیمه'))
    price = models.PositiveBigIntegerField(verbose_name=_('مبلغ قابل پرداخت'))
    prescription_code = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('کد نسخه‌ی پزشک دیگر'))
    experiment_code = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('کدرهگیری(کدملی)'))
    turn = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('نوبت فیزیکی بیمار'))
    is_paid = models.BooleanField(default=False, verbose_name=_('پرداخت شده؟'))
    is_canceled = models.BooleanField(default=False, verbose_name=_('آیا از سمت بیمار کنسل شده است؟'))
    is_returned = models.BooleanField(default=False, verbose_name=_('آیا مبلغ کنسل شدن به بیمار واریز شده است؟'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _('نوبت بیمار')
        verbose_name_plural = _('نوبت بیماران')

    def __str__(self):
        return f'{self.patient.first_name} {self.patient.last_name}'


class ElectronicPrescriptionModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    patient = models.ForeignKey(to=PatientModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بیمار'))
    doctor = models.ForeignKey(to='hospital_doctor.DoctorModel', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('پزشک'))
    unit = models.ForeignKey(to=UnitModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('بخش'))
    experiment_code = models.CharField(max_length=30, verbose_name=_('کدرهگیری(کدملی)'))
    selected_date = models.DateField(blank=True, null=True, verbose_name=_('تاریخ نوبت'))
    selected_time = models.CharField(max_length=15, blank=True, null=True, choices=TIMES, verbose_name=_('ساعت'))
    created = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(default=False, verbose_name=_('آیا این نوبت ثبت شده است؟'))

    class Meta:
        ordering = ['-created']
        verbose_name = _('نوبت نسخه‌ی الکترونیکی بیمار')
        verbose_name_plural = _('نوبت نسخه‌ی الکترونیکی بیماران')

    def __str__(self):
        return f'{self.patient.first_name} {self.patient.last_name}'


class OnlinePaymentModel(models.Model):
    payer = models.ForeignKey(to=PatientTurnModel, on_delete=models.SET_NULL, null=True, verbose_name=_('پرداخت کننده'))
    price = models.PositiveBigIntegerField(verbose_name=_('مبلغ پرداختی'))
    is_success = models.BooleanField(default=False, verbose_name=_('آیا تراکنش موفقیت‌آمیز بوده است؟'))
    code = models.CharField(max_length=50, verbose_name=_('شماره پرداخت'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('پرداخت اینترنتی')
        verbose_name_plural = _('پرداخت‌های اینترنتی')

    def __str__(self):
        return self.payer


class LimitTurnTimeModel(models.Model):
    hours = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('تا چند ساعت قبل؟'))
    rules = RichTextField(blank=True, null=True, verbose_name=_('قوانین نوبت‌دهی'), help_text=_('این قوانین در صفحه‌ی اول قبل از انجام مراحل رزرو اینترنتی نمایش داده میشود.'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('حد‌زمانی برای انتخاب نوبت')
        verbose_name_plural = _('حد‌زمانی برای انتخاب نوبت')

    def __str__(self):
        return str(_('این جدول باید یک مقدار داشته باشد.'))


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