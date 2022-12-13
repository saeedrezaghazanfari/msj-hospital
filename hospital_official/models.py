from django.db import models
from django.utils.translation import gettext_lazy as _


class OrganModel(models.Model):
    TYPE_EX = (
        ('workers', _('کارکنان')), 
        ('it', _('واحد آی تی')),
        ('gaurd', _('حراست')),
        ('engineer', _('فنی')),
        ('aid', _('مددکاری')),
        ('official', _('اداری')),
        ('managering_group', _('هیات مدیره')),
        ('boss', _('ریاست')),
        ('management', _('مدیریت')),
        ('committe', _('کمیته ها')),
    )
    type = models.CharField(max_length=20, choices=TYPE_EX, verbose_name=_('نوع ارگان'))
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('نام'))
    desc = models.TextField(blank=True, null=True, verbose_name=_('متن'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    inside = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('داخلی'))
    address = models.CharField(max_length=255, verbose_name=_('آدرس'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('ارگان')
        verbose_name_plural = _('ارگان ها')

    def __str__(self):
        return self.type


class OrganItemModel(models.Model):
    organ = models.ForeignKey(to=OrganModel, on_delete=models.CASCADE, verbose_name=_('ارگان'))
    first_name = models.CharField(max_length=50, verbose_name=_('نام'))
    last_name = models.CharField(max_length=50, verbose_name=_('نام خانوادگی'))
    national_code = models.CharField(max_length=10, unique=True, verbose_name=_('کدملی'))
    phone = models.CharField(max_length=20, default=0, verbose_name=_('شماره تلفن'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('ایمیل'))
    job = models.CharField(max_length=50, verbose_name=_('سمت'))
    address = models.CharField(max_length=255, verbose_name=_('آدرس'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('عضو ارگان')
        verbose_name_plural = _('اعضای ارگان')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
