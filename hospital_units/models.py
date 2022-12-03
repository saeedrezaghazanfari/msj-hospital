from django.db import models
from Extentions.utils import units_image_path
from django.utils.translation import gettext_lazy as _


class ClinicModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام درمانگاه'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('درمانگاه')
        verbose_name_plural = _('درمانگاه ها')

    def __str__(self):
        return self.title


class SurgeryRoomModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('اتاق عمل')
        verbose_name_plural = _('اتاق های عمل')

    def __str__(self):
        return self.title


class DepartmentModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('دپارتمان')
        verbose_name_plural = _('دپارتمان ها')

    def __str__(self):
        return self.title


class TreatmentSectionModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('بخش درمان')
        verbose_name_plural = _('بخش های درمان')

    def __str__(self):
        return self.title


class ParaclinicModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    inside = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('داخلی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('پاراکلینیک')
        verbose_name_plural = _('پاراکلینیک ها')

    def __str__(self):
        return self.title


class ImagingModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    inside = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('داخلی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تصویربرداری')
        verbose_name_plural = _('تصویربرداری ها')

    def __str__(self):
        return self.title


class LaboratoryModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    inside = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('داخلی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('آزمایشگاه')
        verbose_name_plural = _('آزمایشگاه ها')

    def __str__(self):
        return self.title


class PhysiotherapyModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    inside = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('داخلی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('فیزیوتراپی')
        verbose_name_plural = _('فیزیوتراپی ها')

    def __str__(self):
        return self.title


class PharmacyModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    inside = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('داخلی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('داروخانه')
        verbose_name_plural = _('داروخانه ها')

    def __str__(self):
        return self.title


class AngiographyAngioplastyModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    inside = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('داخلی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('آنژیوگرافی و آنژیوپلاستی')
        verbose_name_plural = _('آنژیوگرافی و آنژیوپلاستی ها')

    def __str__(self):
        return self.title


class EmergencyModel(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('نام'))
    desc = models.TextField(verbose_name=_('متن'))
    image = models.ImageField(upload_to=units_image_path, blank=True, null=True, verbose_name=_('تصویر'))
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('تلفن'))
    inside = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('داخلی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('اورژانس')
        verbose_name_plural = _('اورژانس ها')

    def __str__(self):
        return self.title