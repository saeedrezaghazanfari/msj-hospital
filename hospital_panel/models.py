from email.policy import default
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from hospital_doctor.models import DoctorModel
from extentions.utils import jalali_convertor
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
    insurance = models.ManyToManyField(to=InsuranceModel, verbose_name=_('بیمه ها'))
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