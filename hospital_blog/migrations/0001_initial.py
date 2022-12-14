# Generated by Django 4.1.3 on 2022-12-14 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import extentions.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogGalleryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.blog_gallery_image_path, verbose_name='تصویر')),
                ('video_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='لینک ویدیو')),
            ],
            options={
                'verbose_name': 'گالری بلاگ',
                'verbose_name_plural': 'گالری بلاگ ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='MedicalNoteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=400, verbose_name='متن')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'نوت پزشکی',
                'verbose_name_plural': 'نوت های پزشکی',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': 'تگ',
                'verbose_name_plural': 'تگ ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='BlogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default=extentions.utils.get_blog_code, unique=True, verbose_name='مقدار در url')),
                ('image', models.ImageField(upload_to=extentions.utils.blog_image_path, verbose_name='تصویر')),
                ('video_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='لینک ویدیو')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('read_time', models.PositiveIntegerField(default=0, verbose_name='زمان خواندن')),
                ('desc', models.TextField(verbose_name='متن مقاله')),
                ('short_desc', models.CharField(max_length=500, verbose_name='متن کوتاه')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان انتشار پست')),
                ('is_activate', models.BooleanField(default=False, verbose_name='آیا پست از نظر تولید کننده محتوا تایید شده است؟')),
                ('is_likeable', models.BooleanField(default=True, verbose_name='امکان لایک دارد؟')),
                ('is_dislikeable', models.BooleanField(default=True, verbose_name='امکان دیسلایک دارد؟')),
                ('is_commentable', models.BooleanField(default=True, verbose_name='امکان کامنت دارد؟')),
                ('is_educational', models.BooleanField(default=False, verbose_name='آیا این بلاگ آموزشی است؟')),
                ('categories', models.ManyToManyField(to='hospital_blog.categorymodel', verbose_name='دسته بندی ها')),
                ('gallery', models.ManyToManyField(to='hospital_blog.bloggallerymodel', verbose_name='گالری بلاگ')),
                ('tags', models.ManyToManyField(to='hospital_blog.tagmodel', verbose_name='تگ ها')),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
            options={
                'verbose_name': 'بلاگ',
                'verbose_name_plural': 'بلاگ\u200cها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='BlogLikeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_dislike', models.CharField(choices=[('like', 'لایک'), ('dislike', 'دیسلایک')], max_length=10, verbose_name='لایک یا دیسلایک')),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_blog.blogmodel', verbose_name='بلاگ')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'لایک یا دیسلایک بلاگ',
                'verbose_name_plural': 'لایک یا دیسلایک بلاگ ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='BlogCommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='نظر')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_show', models.BooleanField(default=False, verbose_name='نمایش داده شود؟')),
                ('is_read', models.BooleanField(default=False, verbose_name='توسط نویسنده خوانده شده؟')),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_blog.blogmodel', verbose_name='بلاگ')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_blog.blogcommentmodel', verbose_name='پاسخ')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نظر کاربر برای بلاگ',
                'verbose_name_plural': 'نظرات کاربران برای بلاگ ها',
                'ordering': ['-id'],
            },
        ),
    ]
