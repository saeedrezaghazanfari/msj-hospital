from email.policy import default
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from hospital_auth.models import User, PatientModel
from hospital_units.models import UnitModel
from hospital_doctor.models import TitleSkillModel, DegreeModel
from extentions.utils import (
    jalali_convertor, 
    resume_image_path, 
    workshop_image_path, 
    career_image_path,
    career_code,
    criticic_suggestion_code,
)


class NotificationModel(models.Model): #TODO is_from_boss fk to riast
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    description = models.CharField(max_length=500, verbose_name=_('متن'))
    is_from_boss = models.BooleanField(default=False, verbose_name=_('آیا این متن از سمت ریاست است؟'))
    publish_time = models.DateTimeField(default=timezone.now, verbose_name=_('زمان انتشار پست'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('اعلان')
        verbose_name_plural = _('اعلانات')

    def __str__(self):
        return self.title

    def j_publish_time(self):
        return jalali_convertor(time=self.publish_time, output='j_date')
    j_publish_time.short_description = _('تاریخ انتشار')


class NotificationUserModel(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('کاربر'))
    notification = models.ForeignKey(to=NotificationModel, null=True, on_delete=models.SET_NULL, verbose_name=_('اعلان'))
    is_read = models.BooleanField(default=False, verbose_name=_('توسط کاربر خوانده شده؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('اعلان برای کاربر')
        verbose_name_plural = _('اعلان برای کاربران')

    def __str__(self):
        return str(self.id)


class PatientSightModel(models.Model):
    patient = models.ForeignKey(to=PatientModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بیمار'))
    unit = models.ForeignKey(to=UnitModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بخش'))
    desc = models.TextField(verbose_name=_('متن'))
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name = _('دیدگاه بیمار')
        verbose_name_plural = _('دیدگاه بیماران')

    def __str__(self):
        return self.patient


class BeneficiaryCommentModel(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))
    desc = models.TextField(verbose_name=_('متن'))
    bio = models.TextField(blank=True, null=True, verbose_name=_('بیوگرافی'))
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name = _('نظر ذینفع')
        verbose_name_plural = _('نظرات ذینفعان')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ContactUsModel(models.Model):
    message = models.TextField(verbose_name=_('متن ارتباط'))
    name = models.CharField(max_length=100, verbose_name=_('نام و نام خانوادگی'))
    email = models.EmailField(max_length=100, verbose_name=_('ایمیل کاربر'))
    phone = models.BigIntegerField(verbose_name=_('شماره تلفن'))
    title = models.CharField(max_length=100, verbose_name=_('عنوان ارتباط'))
    is_read = models.BooleanField(default=False, verbose_name=_('بررسی شده یا نه'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('تماس مخاطب')
        verbose_name_plural = _('تماس های مخاطبان')

    def __str__(self):
        return str(self.title)

    def j_created(self):
        return jalali_convertor(time=self.created, output='j_date')
    j_created.short_description = _('تاریخ انتشار')


class CriticismSuggestionModel(models.Model):
    code = models.CharField(default=criticic_suggestion_code, max_length=20, verbose_name=_('کد پیگیری'))
    message = models.TextField(verbose_name=_('متن ارتباط'))
    first_name = models.CharField(max_length=100, verbose_name=_('نام بیمار'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی بیمار'))
    national_code = models.PositiveBigIntegerField(verbose_name=_('کدملی بیمار'))
    email = models.EmailField(max_length=100, verbose_name=_('ایمیل کاربر'))
    phone = models.BigIntegerField(verbose_name=_('شماره تلفن'))
    manager = models.CharField(max_length=100, verbose_name=_('نام مسیول'))
    unit = models.ForeignKey(to=UnitModel, on_delete=models.SET_NULL, null=True, verbose_name=_('نام بخش'))
    is_read = models.BooleanField(default=False, verbose_name=_('بررسی شده یا نه'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('انتقاد و پیشنهاد مخاطب')
        verbose_name_plural = _('انتقادات و پیشنهادات مخاطبان')

    def __str__(self):
        return str(self.national_code)


class PeopleAidModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('نام و نام خانوادگی'))
    email = models.EmailField(max_length=100, verbose_name=_('ایمیل کاربر'))
    phone = models.BigIntegerField(verbose_name=_('شماره تلفن'))
    price = models.PositiveBigIntegerField(verbose_name=_('مبلغ کمک شده'))
    date_of_aid = models.DateTimeField(default=timezone.now, verbose_name=_('تاریخ کمک'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('کمک مردمی')
        verbose_name_plural = _('کمک های مردمی')

    def __str__(self):
        return str(self.name)

    def j_date_of_aid(self):
        return jalali_convertor(time=self.date_of_aid, output='j_date')
    j_date_of_aid.short_description = _('تاریخ انتشار')


class BenefactorModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('نام و نام خانوادگی'))
    is_founder = models.BooleanField(default=False, verbose_name=_('بنیانگذار است؟'))
    about = models.TextField(verbose_name=_('درباره ی نیکوکار'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('خیر و نیکوکار')
        verbose_name_plural = _('خیرین و نیکوکاران')

    def __str__(self):
        return str(self.name)


class CareersModel(models.Model):    
    GENDER_USER = (('male', _('مرد')), ('female', _('زن')))
    code = models.CharField(default=career_code, max_length=20, verbose_name=_('کد موقعیت شغلی'))
    unit = models.ForeignKey(to=UnitModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بخش مربوطه'))
    skill = models.ForeignKey(to=TitleSkillModel, on_delete=models.SET_NULL, null=True, verbose_name=_('تخصص'))
    degree = models.ForeignKey(to=DegreeModel, on_delete=models.SET_NULL, null=True, verbose_name=_('نوع مدرک'))
    gender = models.CharField(choices=GENDER_USER, max_length=7, verbose_name=_('جنسیت'))
    title = models.CharField(max_length=100, verbose_name=_('عنوان موقعیت'))
    desc = models.TextField(verbose_name=_('توضیحات'))
    min_age = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('حداقل سن'))
    max_age = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('حداکثر سن'))
    image = models.ImageField(upload_to=career_image_path, verbose_name=_('تصویر'))
    expriment = models.TextField(verbose_name=_('تجربه ی مورد نیاز'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال؟'))


    class Meta:
        ordering = ['-id']
        verbose_name = _('موقعیت شغلی بیمارستان')
        verbose_name_plural = _('موقعیت های شغلی بیمارستان')

    def __str__(self):
        return str(self.code)


class HireFormModel(models.Model):
    SINGLE_MARRIED = (('single', _('مجرد')), ('married', _('متاهل')))
    SOLDIERING_TYPE = (('end', _('پایان خدمت')), ('abs_exemption', _('معافیت دایم')), ('edu_exemption', _('معافیت تحصیلی')), ('progressing', _('در حال انجام')), ('include', _('مشمول')))
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('کاربر'))
    career = models.ForeignKey(to=CareersModel, on_delete=models.SET_NULL, null=True, verbose_name=_('موقعیت شغلی'))
    created = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False, verbose_name=_('آیا بررسی شده است؟'))

    first_name = models.CharField(max_length=50, verbose_name=_('نام'))
    last_name = models.CharField(max_length=50, verbose_name=_('نام خانوادگی'))
    father = models.CharField(max_length=50, verbose_name=_('نام پدر'))
    national_code = models.CharField(max_length=10, unique=True, verbose_name=_('کدملی'))
    national_number = models.CharField(max_length=20, verbose_name=_('شماره شناسنامه'))
    burthday_date = models.DateField(verbose_name=_('تاریخ تولد'))
    burthday_place = models.CharField(max_length=50, verbose_name=_('محل تولد'))
    single_married = models.CharField(choices=SINGLE_MARRIED, max_length=10, verbose_name=_('وضعیت تاهل'))
    num_childs = models.PositiveIntegerField(default=0, verbose_name=_('تعداد فرزندان'))
    soldiering = models.CharField(max_length=20, choices=SOLDIERING_TYPE, verbose_name=_('وضعیت نظام وظیفه'))
    end_date = models.DateField(verbose_name=_('تاریخ پایان طرح'))
    direct = models.CharField(max_length=50, verbose_name=_('معرف'))
    education = models.CharField(max_length=50, verbose_name=_('تحصیلات'))
    uni = models.CharField(max_length=50, verbose_name=_('نام دانشگاه'))
    address = models.TextField(verbose_name=_('آدرس محل زندگی'))
    phone = models.CharField(max_length=20, default=0, verbose_name=_('شماره تلفن'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('ایمیل'))
    resume = models.FileField(upload_to=resume_image_path, verbose_name=_('رزومه کاری مرتبط با کار درخواستی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('فرم های استخدام')
        verbose_name_plural = _('فرم های استخدام')

    def __str__(self):
        return self.user


class WorkshopModel(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('عنوان'))
    length = models.CharField(max_length=50, verbose_name=_('طول دوره'))
    category = models.CharField(max_length=100, verbose_name=_('دسته بندی دوره'))
    capacity = models.PositiveIntegerField(verbose_name=_('ظرفیت دوره'))
    nums = models.PositiveIntegerField(verbose_name=_('تعداد شرکت کنندگان'))
    times = models.CharField(max_length=100, verbose_name=_('ساعات برگذاری'))
    proffessors = models.CharField(max_length=255, verbose_name=_('استادان دوره'))
    have_degree = models.BooleanField(default=False, verbose_name=_('آیا این دوره شامل مدرک میشود؟'))
    image = models.ImageField(upload_to=workshop_image_path, verbose_name=_('تصویر'))
    start_date = models.DateField(verbose_name=_('تاریخ شروع دوره'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('کارگاه و دوره آموزشی')
        verbose_name_plural = _('کارگاه ها و دوره های آموزشی')

    def __str__(self):
        return self.title

