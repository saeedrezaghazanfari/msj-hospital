from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from hospital_auth.models import User, ContentProducerModel
from Extentions.utils import (
    jalali_convertor, 
    news_image_path, 
    get_news_code, 
    news_gallery_image_path,
)


class NewsModel(models.Model):
    slug = models.SlugField(unique=True, default=get_news_code, verbose_name=_('مقدار در url'))
    image = models.ImageField(upload_to=news_image_path, verbose_name=_('تصویر'))
    video = models.FileField(upload_to=news_image_path, null=True, blank=True, verbose_name=_('ویدیو'))
    writer_contentproducer = models.ForeignKey(to=ContentProducerModel, on_delete=models.CASCADE, verbose_name=_('نویسنده'))
    categories = models.ManyToManyField(to='CategoryModel', verbose_name=_('دسته بندی ها'))
    tags = models.ManyToManyField(to='TagModel', verbose_name=_('تگ ها'))
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    desc = models.TextField(verbose_name=_('متن مقاله'))
    publish_time = models.DateTimeField(default=timezone.now, verbose_name=_('زمان انتشار پست'))
    is_likeable = models.BooleanField(default=True, verbose_name=_('امکان لایک دارد؟'))
    is_dislikeable = models.BooleanField(default=True, verbose_name=_('امکان دیسلایک دارد؟'))
    is_commentable = models.BooleanField(default=True, verbose_name=_('امکان کامنت دارد؟'))
    gallery = models.ManyToManyField('NewsGalleryModel', null=True, blank=True, verbose_name=_('گالری خبر'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('خبر')
        verbose_name_plural = _('خبر‌ها')

    def __str__(self):
        return self.title

    # def j_created(self):
    #     return jalali_convertor(time=self.created, output='j_date')
    # j_created.short_description = _('تاریخ انتشار')

    def j_month(self):
        return jalali_convertor(time=self.created, output='j_month')

    def prev_post(self):
        prev_id = int(self.id) - 1
        news = NewsModel.objects.filter(id=prev_id, is_published=True).first()
        if news:
            return news
        return None

    def next_post(self):
        next_id = int(self.id) + 1
        news = NewsModel.objects.filter(id=next_id, is_published=True).first()
        if news:
            return news
        return None

    def get_full_name(self):
        try:
            return f'{self.writer_contentproducer.user.first_name} {self.writer_contentproducer.user.last_name}'
        except:
            return _('پشتیبان')
    get_full_name.short_description = _('نام نویسنده')


class NewsGalleryModel(models.Model):
    FILE_TYPES = (('video', _('ویدیو')), ('image', _('تصویر')))
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, verbose_name=_('نوع فایل'))
    file = models.FileField(upload_to=news_gallery_image_path, verbose_name=_('فایل'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گالری خبر')
        verbose_name_plural = _('گالری خبرها')

    def __str__(self):
        return self.title


class NewsCommentModel(models.Model):
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('پاسخ'))
    message = models.TextField(verbose_name=_('نظر'))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    news = models.ForeignKey(to=NewsModel, on_delete=models.CASCADE, verbose_name=_('خبر'))
    created = models.DateTimeField(auto_now_add=True)
    is_show = models.BooleanField(default=False, verbose_name=_('نمایش داده شود؟'))
    is_read = models.BooleanField(default=False, verbose_name=_('توسط نویسنده خوانده شده؟'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('نظر کاربر برای خبر') 
        verbose_name_plural = _('نظرات کاربران برای خبرها')

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


class NewsLikeModel(models.Model):
    LIKE_DISLIKE = (('like', _('لایک')), ('dislike', _('دیسلایک')))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    news = models.ForeignKey(to=NewsModel, on_delete=models.CASCADE, verbose_name=_('خبر'))
    like_dislike = models.CharField(choices=LIKE_DISLIKE, max_length=10, verbose_name=_('لایک یا دیسلایک'))
    
    class Meta:
        ordering = ['-id']
        verbose_name = _('لایک یا دیسلایک خبر')
        verbose_name_plural = _('لایک یا دیسلایک خبر ها')

    def __str__(self):
        return str(self.id)

