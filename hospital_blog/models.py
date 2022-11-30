from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from hospital_auth.models import User, ContentProducerModel
from Extentions.utils import (
    jalali_convertor, 
    blog_image_path, 
    get_blog_code, 
    blog_gallery_image_path,

)


# Managers
class BlogModelManager(models.Manager):
    def get_published(self):
        this_time = timezone.now()
        return self.get_queryset().filter(is_activate=True, publish_time__lt=this_time)


# class MedicalNoteModel(models.Model):
#     doctor = models.ForeignKey(to=DoctorModel, on_delete=models.CASCADE, verbose_name=_('پزشک'))
#     short_title = models.CharField(max_length=100, verbose_name=_('عنوان کوتاه'))
#     text = models.TextField(max_length=400, verbose_name=_('متن'))
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-id']
#         verbose_name = _('نوت پزشک')
#         verbose_name_plural = _('نوت های پرشکان')

#     def __str__(self):
#         return self.short_title

#     def get_full_name(self):
#         return f'{self.doctor.user.first_name} {self.doctor.user.last_name}'
#     get_full_name.short_description = _('نام پزشک')


class BlogModel(models.Model):  #TODO
    slug = models.SlugField(unique=True, default=get_blog_code, verbose_name=_('مقدار در url'))
    image = models.ImageField(upload_to=blog_image_path, verbose_name=_('تصویر'))
    video = models.FileField(upload_to=blog_image_path, null=True, blank=True, verbose_name=_('ویدیو'))
    writer_contentproducer = models.ForeignKey(to=ContentProducerModel, on_delete=models.CASCADE, verbose_name=_('نویسنده'), help_text=_('اگر این فیلد پر بشود یعنی تولید کننده ی این پست یک شخص تولید کننده ی محتوا بوده است.'))
    # writer_doctor = models.ForeignKey(to=DoctorModel, on_delete=models.CASCADE, verbose_name=_('نویسنده'), help_text=_('اگر این فیلد پر بشود یعنی تولید کننده ی این پست یک پزشک بوده است.'))
    categories = models.ManyToManyField(to='CategoryModel', verbose_name=_('دسته بندی ها'))
    tags = models.ManyToManyField(to='TagModel', verbose_name=_('تگ ها'))
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    read_time = models.PositiveIntegerField(default=0, verbose_name=_('زمان خواندن'))
    desc = models.TextField(verbose_name=_('متن مقاله'))
    short_desc = models.CharField(max_length=500, verbose_name=_('متن کوتاه'))
    publish_time = models.DateTimeField(default=timezone.now, verbose_name=_('زمان انتشار پست'))
    is_activate = models.BooleanField(default=False, verbose_name=_('آیا پست از نظر تولید کننده محتوا تایید شده است؟'))
    is_likeable = models.BooleanField(default=True, verbose_name=_('امکان لایک دارد؟'))
    is_dislikeable = models.BooleanField(default=True, verbose_name=_('امکان دیسلایک دارد؟'))
    is_commentable = models.BooleanField(default=True, verbose_name=_('امکان کامنت دارد؟'))
    is_educational = models.BooleanField(default=False, verbose_name=_('آیا این بلاگ آموزشی است؟'))
    gallery = models.ManyToManyField('BlogGalleryModel', null=True, blank=True, verbose_name=_('گالری بلاگ'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('بلاگ')
        verbose_name_plural = _('بلاگ‌ها')

    objects = BlogModelManager()

    def __str__(self):
        return self.title

    def j_publish_time(self):
        return jalali_convertor(time=self.publish_time, output='j_date')
    j_publish_time.short_description = _('تاریخ انتشار')

    def prev_post(self):
        prev_id = int(self.id) - 1
        this_time = timezone.now()
        blog = BlogModel.objects.filter(id=prev_id, is_activate=True, publish_time__lt=this_time).first()
        if blog:
            return blog
        return None

    def next_post(self):
        next_id = int(self.id) + 1
        this_time = timezone.now()
        blog = BlogModel.objects.filter(id=next_id, is_activate=True, publish_time__lt=this_time).first()
        if blog:
            return blog
        return None

    def get_full_name(self):
        if self.writer_contentproducer:
            try:
                return f'{self.writer_contentproducer.user.first_name} {self.writer_contentproducer.user.last_name}'
            except:
                return _('پشتیبان')
        elif self.writer_doctor:
            try:
                return f'{self.writer_doctor.user.first_name} {self.writer_doctor.user.last_name}'
            except:
                return _('پشتیبان')
        else:
            return _('پشتیبان')
    get_full_name.short_description = _('نام نویسنده')


class BlogGalleryModel(models.Model):
    FILE_TYPES = (('video', _('ویدیو')), ('image', _('تصویر')))
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, verbose_name=_('نوع فایل'))
    file = models.FileField(upload_to=blog_gallery_image_path, verbose_name=_('فایل'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گالری بلاگ')
        verbose_name_plural = _('گالری بلاگ ها')

    def __str__(self):
        return self.title


class BlogCommentModel(models.Model):
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('پاسخ'))
    message = models.TextField(verbose_name=_('نظر'))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    blog = models.ForeignKey(to=BlogModel, on_delete=models.CASCADE, verbose_name=_('بلاگ'))
    created = models.DateTimeField(auto_now_add=True)
    is_show = models.BooleanField(default=False, verbose_name=_('نمایش داده شود؟'))
    is_read = models.BooleanField(default=False, verbose_name=_('توسط نویسنده خوانده شده؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نظر کاربر برای بلاگ')
        verbose_name_plural = _('نظرات کاربران برای بلاگ ها')

    def j_created(self):
        return jalali_convertor(time=self.created, output='j_date')
    j_created.short_description = _('تاریخ نظر')

    def __str__(self):
        return str(self.id)


class CategoryModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')

    def __str__(self):
        return self.title


class TagModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تگ')
        verbose_name_plural = _('تگ ها')

    def __str__(self):
        return self.title


class BlogLikeModel(models.Model):
    LIKE_DISLIKE = (('like', _('لایک')), ('dislike', _('دیسلایک')))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    blog = models.ForeignKey(to=BlogModel, on_delete=models.CASCADE, verbose_name=_('بلاگ'))
    like_dislike = models.CharField(choices=LIKE_DISLIKE, max_length=10, verbose_name=_('لایک یا دیسلایک'))
    
    class Meta:
        ordering = ['-id']
        verbose_name = _('لایک یا دیسلایک بلاگ')
        verbose_name_plural = _('لایک یا دیسلایک بلاگ ها')

    def __str__(self):
        return str(self.id)

