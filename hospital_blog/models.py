import uuid
from django.db import models
from translated_fields import TranslatedField
from django.utils.translation import gettext_lazy as _
from hospital_auth.models import User
from hospital_units.models import UnitModel
from ckeditor.fields import RichTextField
from extentions.utils import (
    jalali_convertor, 
    blog_image_path,
    blog_pdf_image_path,
    blog_qrcode_image_path,
    get_credit_edu_code, 
    credit_edu_image_path,
    get_blog_code, 
    blog_gallery_image_path,
    pamphelet_image_path
)


# Managers
class BlogModelManager(models.Manager):
    def get_published(self):
        return self.get_queryset().filter(is_publish=True)


class MedicalNoteModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    text = TranslatedField(models.TextField(max_length=400, verbose_name=_('متن')))
    is_active = models.BooleanField(default=False, verbose_name=_('فعال/غیرفعال'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('نوت پزشکی')
        verbose_name_plural = _('نوت های پزشکی')

    def j_created(self):
        return jalali_convertor(time=self.created, output='j_date')
    j_created.short_description = _('تاریخ انتشار')

    def __str__(self):
        return str(self.id)


class PampheletModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    image = models.ImageField(upload_to=pamphelet_image_path, verbose_name=_('تصویر'))
    title = TranslatedField(models.CharField(max_length=200, verbose_name=_('عنوان')))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('پمفلت آموزشی')
        verbose_name_plural = _('پمفلت های آموزشی')

    def __str__(self):
        return self.title


class CreditEduModel(models.Model):
    slug = models.SlugField(unique=True, default=get_credit_edu_code, verbose_name=_('مقدار در url'))
    title = TranslatedField(models.CharField(max_length=200, verbose_name=_('عنوان')))
    image = models.ImageField(upload_to=credit_edu_image_path, verbose_name=_('تصویر'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('آموزش اعتبار بخشی')
        verbose_name_plural = _('آموزش های اعتباربخشی')

    def __str__(self):
        return self.title


class BlogModel(models.Model):
    slug = models.SlugField(unique=True, default=get_blog_code, verbose_name=_('مقدار در url'))
    image = models.ImageField(upload_to=blog_image_path, verbose_name=_('تصویر'))
    pdf = models.FileField(upload_to=blog_pdf_image_path, blank=True, null=True, verbose_name=_('پی دی اف بلاگ'))
    qr_img = models.ImageField(upload_to=blog_qrcode_image_path, blank=True, null=True, verbose_name=_('تصویر کد QR'))
    video_link = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('لینک ویدیو'))
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('نویسنده'))
    categories = models.ManyToManyField(to='CategoryModel', verbose_name=_('دسته بندی ها'))
    tags = models.ManyToManyField(to='TagModel', verbose_name=_('تگ ها'))
    title = TranslatedField(models.CharField(max_length=200, verbose_name=_('عنوان')))
    read_time = models.PositiveIntegerField(default=0, verbose_name=_('زمان خواندن'))
    desc = TranslatedField(RichTextField(verbose_name=_('متن مقاله')))
    short_desc = TranslatedField(models.TextField(max_length=500, verbose_name=_('متن کوتاه')))
    is_publish = models.BooleanField(default=False, verbose_name=_('آیا منتشر شود؟'))
    is_emailed = models.BooleanField(default=False, editable=False, verbose_name=_('آیا ایمیل شده است؟'))
    is_likeable = models.BooleanField(default=True, verbose_name=_('امکان لایک دارد؟'))
    is_dislikeable = models.BooleanField(default=True, verbose_name=_('امکان دیسلایک دارد؟'))
    is_commentable = models.BooleanField(default=True, verbose_name=_('امکان کامنت دارد؟'))
    gallery = models.ManyToManyField('BlogGalleryModel', blank=True, verbose_name=_('گالری بلاگ'))
    units = models.ManyToManyField(to=UnitModel, blank=True, verbose_name=_('بخش ها'))
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _('بلاگ')
        verbose_name_plural = _('بلاگ‌ها')

    objects = BlogModelManager()

    def __str__(self):
        return self.title

    def j_created(self):
        return jalali_convertor(time=self.created, output='j_date')
    j_created.short_description = _('تاریخ انتشار')

    def j_month(self):
        return jalali_convertor(time=self.created, output='j_month')

    def prev_post(self):
        blog = BlogModel.objects.filter(id__lt=self.id).order_by('id').first()
        if blog:
            return blog
        return None

    def next_post(self):
        blog = BlogModel.objects.filter(id__gt=self.id).order_by('id').first()
        if blog:
            return blog
        return None

    def get_full_name(self):
        return f'{self.writer.firstname()} {self.writer.lastname()}'
    get_full_name.short_description = _('نام نویسنده')


class BlogGalleryModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    image = models.ImageField(upload_to=blog_gallery_image_path, null=True, blank=True, verbose_name=_('تصویر'))
    video_link = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('لینک ویدیو'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گالری بلاگ')
        verbose_name_plural = _('گالری بلاگ ها')

    def __str__(self):
        return self.title


class BlogCommentModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('پاسخ'))
    message = RichTextField(verbose_name=_('نظر'))
    first_name = models.CharField(max_length=255, null=True, verbose_name=_('نام'))
    last_name = models.CharField(max_length=255, null=True, verbose_name=_('نام خانوادگی'))
    phone = models.CharField(max_length=20, null=True, verbose_name=_('شماره تلفن'))
    blog = models.ForeignKey(to=BlogModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بلاگ'))
    created = models.DateTimeField(auto_now_add=True)
    is_show = models.BooleanField(default=False, verbose_name=_('نمایش داده شود؟'))
    is_read = models.BooleanField(default=False, verbose_name=_('توسط نویسنده خوانده شده؟'))

    class Meta:
        ordering = ['-created']
        verbose_name = _('نظر کاربر برای بلاگ')
        verbose_name_plural = _('نظرات کاربران برای بلاگ ها')

    def j_created(self):
        return jalali_convertor(time=self.created, output='j_date')
    j_created.short_description = _('تاریخ نظر')

    def __str__(self):
        return str(self.id)


class CategoryModel(models.Model):
    title = TranslatedField(models.CharField(max_length=100, verbose_name=_('عنوان')))

    class Meta:
        ordering = ['-id']
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')

    def __str__(self):
        return self.title


class TagModel(models.Model):
    title = TranslatedField(models.CharField(max_length=100, verbose_name=_('عنوان')))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تگ')
        verbose_name_plural = _('تگ ها')

    def __str__(self):
        return self.title


class BlogLikeModel(models.Model):
    LIKE_DISLIKE = (('like', _('لایک')), ('dislike', _('دیسلایک')))
    user_ip = models.GenericIPAddressField(null=True)
    blog = models.ForeignKey(to=BlogModel, on_delete=models.SET_NULL, null=True, verbose_name=_('بلاگ'))
    like_dislike = models.CharField(choices=LIKE_DISLIKE, max_length=10, verbose_name=_('لایک یا دیسلایک'))
    
    class Meta:
        ordering = ['-id']
        verbose_name = _('لایک یا دیسلایک بلاگ')
        verbose_name_plural = _('لایک یا دیسلایک بلاگ ها')

    def __str__(self):
        return str(self.id)

