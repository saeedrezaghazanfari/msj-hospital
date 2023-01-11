from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField
from hospital_auth.models import User
from hospital_units.models import UnitModel
from hospital_blog.models import TagModel, CategoryModel
from extentions.utils import (
    jalali_convertor, 
    news_image_path, 
    get_news_code, 
    news_gallery_image_path,
)


# Managers
class NewsModelManager(models.Manager):
    def get_published(self):
        this_time = timezone.now()
        return self.get_queryset().filter(publish_time__lt=this_time)


class NewsModel(models.Model):
    slug = models.SlugField(unique=True, default=get_news_code, verbose_name=_('مقدار در url'))
    image = models.ImageField(upload_to=news_image_path, verbose_name=_('تصویر'))
    video_link = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('لینک ویدیو'))
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('نویسنده'))
    categories = models.ManyToManyField(to=CategoryModel, verbose_name=_('دسته بندی ها'))
    tags = models.ManyToManyField(to=TagModel, verbose_name=_('تگ ها'))
    title = TranslatedField(models.CharField(max_length=200, verbose_name=_('عنوان')))
    desc = TranslatedField(models.TextField(verbose_name=_('متن مقاله')))
    is_publish = models.BooleanField(default=False, verbose_name=_('آیا منتشر شود؟'))
    is_emailed = models.BooleanField(default=False, verbose_name=_('آیا ایمیل شده است؟'))
    is_likeable = models.BooleanField(default=True, verbose_name=_('امکان لایک دارد؟'))
    is_dislikeable = models.BooleanField(default=True, verbose_name=_('امکان دیسلایک دارد؟'))
    is_commentable = models.BooleanField(default=True, verbose_name=_('امکان کامنت دارد؟'))
    gallery = models.ManyToManyField('NewsGalleryModel', verbose_name=_('گالری خبر'))
    units = models.ManyToManyField(to=UnitModel, verbose_name=_('بخش ها'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('خبر')
        verbose_name_plural = _('خبر‌ها')

    objects = NewsModelManager()

    def __str__(self):
        return self.title

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
        return f'{self.writer.user.firstname()} {self.writer.user.lastname()}'
    get_full_name.short_description = _('نام نویسنده')


class NewsGalleryModel(models.Model):
    title = TranslatedField(models.CharField(max_length=100, verbose_name=_('عنوان')))
    image = models.ImageField(upload_to=news_gallery_image_path, null=True, blank=True, verbose_name=_('تصویر'))
    video_link = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('لینک ویدیو'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('گالری خبر')
        verbose_name_plural = _('گالری خبرها')

    def __str__(self):
        return self.title


class NewsCommentModel(models.Model):
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('پاسخ'))
    message = models.TextField(verbose_name=_('نظر'))
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('کاربر'))
    news = models.ForeignKey(to=NewsModel, on_delete=models.SET_NULL, null=True, verbose_name=_('خبر'))
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


class NewsLikeModel(models.Model):
    LIKE_DISLIKE = (('like', _('لایک')), ('dislike', _('دیسلایک')))
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name=_('کاربر'))
    news = models.ForeignKey(to=NewsModel, on_delete=models.SET_NULL, null=True, verbose_name=_('خبر'))
    like_dislike = models.CharField(choices=LIKE_DISLIKE, max_length=10, verbose_name=_('لایک یا دیسلایک'))
    
    class Meta:
        ordering = ['-id']
        verbose_name = _('لایک یا دیسلایک خبر')
        verbose_name_plural = _('لایک یا دیسلایک خبر ها')

    def __str__(self):
        return str(self.id)

