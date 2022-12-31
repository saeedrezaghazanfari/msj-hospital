# Generated by Django 4.1.3 on 2022-12-31 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import extentions.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospital_blog', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital_units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsGalleryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.news_gallery_image_path, verbose_name='تصویر')),
                ('video_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='لینک ویدیو')),
            ],
            options={
                'verbose_name': 'گالری خبر',
                'verbose_name_plural': 'گالری خبرها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='NewsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default=extentions.utils.get_news_code, unique=True, verbose_name='مقدار در url')),
                ('image', models.ImageField(upload_to=extentions.utils.news_image_path, verbose_name='تصویر')),
                ('video_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='لینک ویدیو')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('desc', models.TextField(verbose_name='متن مقاله')),
                ('is_publish', models.BooleanField(default=False, verbose_name='آیا منتشر شود؟')),
                ('is_emailed', models.BooleanField(default=False, verbose_name='آیا ایمیل شده است؟')),
                ('is_likeable', models.BooleanField(default=True, verbose_name='امکان لایک دارد؟')),
                ('is_dislikeable', models.BooleanField(default=True, verbose_name='امکان دیسلایک دارد؟')),
                ('is_commentable', models.BooleanField(default=True, verbose_name='امکان کامنت دارد؟')),
                ('categories', models.ManyToManyField(to='hospital_blog.categorymodel', verbose_name='دسته بندی ها')),
                ('gallery', models.ManyToManyField(to='hospital_news.newsgallerymodel', verbose_name='گالری خبر')),
                ('tags', models.ManyToManyField(to='hospital_blog.tagmodel', verbose_name='تگ ها')),
                ('units', models.ManyToManyField(to='hospital_units.unitmodel', verbose_name='بخش ها')),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
            options={
                'verbose_name': 'خبر',
                'verbose_name_plural': 'خبر\u200cها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='NewsLikeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_dislike', models.CharField(choices=[('like', 'لایک'), ('dislike', 'دیسلایک')], max_length=10, verbose_name='لایک یا دیسلایک')),
                ('news', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_news.newsmodel', verbose_name='خبر')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'لایک یا دیسلایک خبر',
                'verbose_name_plural': 'لایک یا دیسلایک خبر ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='NewsCommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='نظر')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_show', models.BooleanField(default=False, verbose_name='نمایش داده شود؟')),
                ('is_read', models.BooleanField(default=False, verbose_name='توسط نویسنده خوانده شده؟')),
                ('news', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_news.newsmodel', verbose_name='خبر')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_news.newscommentmodel', verbose_name='پاسخ')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نظر کاربر برای خبر',
                'verbose_name_plural': 'نظرات کاربران برای خبرها',
                'ordering': ['-id'],
            },
        ),
    ]
