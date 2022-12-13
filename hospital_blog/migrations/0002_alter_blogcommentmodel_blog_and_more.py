# Generated by Django 4.1.3 on 2022-12-13 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcommentmodel',
            name='blog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_blog.blogmodel', verbose_name='بلاگ'),
        ),
        migrations.AlterField(
            model_name='blogcommentmodel',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_blog.blogcommentmodel', verbose_name='پاسخ'),
        ),
        migrations.AlterField(
            model_name='blogcommentmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='bloglikemodel',
            name='blog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_blog.blogmodel', verbose_name='بلاگ'),
        ),
        migrations.AlterField(
            model_name='bloglikemodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده'),
        ),
    ]
