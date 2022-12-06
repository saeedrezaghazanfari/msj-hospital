from email.policy import default
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from hospital_doctor.models import DoctorModel
from hospital_auth.models import User
from extentions.utils import jalali_convertor, get_patient_tracking_code
from hospital_setting.models import InsuranceModel


class AppointmentTimeListModel(models.Model): #TODO part
    PART_NAMES = (('', _('')), ('', _('')))
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
    part_name = models.CharField(max_length=20, blank=True, null=True, choices=PART_NAMES, verbose_name=_('نام بخش'))
    doctor = models.ForeignKey(DoctorModel, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('پزشک'))
    date = models.DateField(default=timezone.now, verbose_name=_('تاریخ روز'))
    time = models.CharField(max_length=15, choices=TIMES, verbose_name=_('بازه ی زمانی'))
    insurances = models.ManyToManyField(to=InsuranceModel, verbose_name=_('بیمه ها'))
    time_of_one_visit = models.PositiveIntegerField(default=5, verbose_name=_('زمان ویزیت هر بیمار با این بخش/پزشک'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('زمان نوبتدهی')
        verbose_name_plural = _('لیست زمان های نوبتدهی')

    def __str__(self):
        return str(self.id)

    def j_date(self):
        return jalali_convertor(time=self.date, number=True)
    j_date.short_description = _('تاریخ روز')


class PatientTurnModel(models.Model):
    tracking_code = models.PositiveIntegerField(default=get_patient_tracking_code, verbose_name=_('کد پیگیری'))
    appointment_time = models.ForeignKey(to=AppointmentTimeListModel, on_delete=models.CASCADE, verbose_name=_('زمان نوبتدهی'))
    full_name = models.CharField(max_length=50, verbose_name=_('نام بیمار'))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('درخواست کننده'))
    insurance = models.CharField(max_length=100, verbose_name=_('بیمه ها'))
    is_visited = models.BooleanField(default=False, verbose_name=_('آیا ویزیت شده است؟'))
    is_paid = models.BooleanField(default=False, verbose_name=_('آیا پرداخت شده است؟'))
    is_read_rules = models.BooleanField(default=False, verbose_name=_('آیا قوانین را خوانده است؟'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('نوبت بیمار')
        verbose_name_plural = _('نوبت بیماران')

    def __str__(self):
        return self.full_name

    def j_created(self):
        return jalali_convertor(time=self.created, number=True)
    j_created.short_description = _('زمان ثبت درخواست')


class UserElectronicPaymentModel(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    price = models.PositiveBigIntegerField(verbose_name=_('مبلغ'))
    tracking_code = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('شماره پرداخت'))
    is_success = models.BooleanField(default=False, verbose_name=_('آیا موفق بوده است؟'))
    created = models.DateTimeField(default=timezone.now, verbose_name=_('زمان ثبت تراکنش'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('پرداخت الکترونیکی کاربر')
        verbose_name_plural = _('پرداخت الکترونیکی کاربران')

    def __str__(self):
        return self.user

    def j_created(self):
        return jalali_convertor(time=self.created, number=True)
    j_created.short_description = _('زمان ثبت تراکنش')

