from email.policy import default
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from hospital_auth.models import User
from Extentions.utils import jalali_convertor


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
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    notification = models.ForeignKey(to=NotificationModel, on_delete=models.CASCADE, verbose_name=_('اعلان'))
    is_read = models.BooleanField(default=False, verbose_name=_('توسط کاربر خوانده شده؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('اعلان برای کاربر')
        verbose_name_plural = _('اعلان برای کاربران')

    def __str__(self):
        return str(self.id)


# class PatientSightModel(models.Model):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
#     desc = models.TextField(verbose_name=_('متن'))
#     created = models.DateTimeField(auto_now_add=True)
#     is_show = models.BooleanField(default=False, verbose_name=_('فعال/غیرفعال'))
    
#     class Meta:
#         ordering = ['-id']
#         verbose_name = _('دیدگاه بیمار')
#         verbose_name_plural = _('دیدگاه بیماران')

#     def __str__(self):
#         return self.user


# class CooperationModel(models.Model):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))

#     class Meta:
#         ordering = ['-id']
#         verbose_name = _('همکاری')
#         verbose_name_plural = _('همکاری ها')

#     def __str__(self):
#         return self.user


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


# class CriticismSuggestionModel(models.Model):
#     message = models.TextField(verbose_name=_('متن ارتباط'))
#     name = models.CharField(max_length=100, verbose_name=_('نام و نام خانوادگی'))
#     email = models.EmailField(max_length=100, verbose_name=_('ایمیل کاربر'))
#     phone = models.BigIntegerField(verbose_name=_('شماره تلفن'))
#     title = models.CharField(max_length=100, verbose_name=_('عنوان ارتباط'))
#     is_read = models.BooleanField(default=False, verbose_name=_('بررسی شده یا نه'))
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-id']
#         verbose_name = _('انتقاد و پیشنهاد مخاطب')
#         verbose_name_plural = _('انتقادات و پیشنهادات مخاطبان')

#     def __str__(self):
#         return str(self.title)


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