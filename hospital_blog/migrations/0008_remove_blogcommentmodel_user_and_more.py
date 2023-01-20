# Generated by Django 4.1.3 on 2023-01-20 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_blog', '0007_alter_blogmodel_units'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcommentmodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='bloglikemodel',
            name='user',
        ),
        migrations.AddField(
            model_name='blogcommentmodel',
            name='first_name',
            field=models.CharField(max_length=255, null=True, verbose_name='نام'),
        ),
        migrations.AddField(
            model_name='blogcommentmodel',
            name='last_name',
            field=models.CharField(max_length=255, null=True, verbose_name='نام خانوادگی'),
        ),
        migrations.AddField(
            model_name='blogcommentmodel',
            name='phone',
            field=models.CharField(max_length=20, null=True, verbose_name='شماره تلفن'),
        ),
        migrations.AddField(
            model_name='bloglikemodel',
            name='user_ip',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='gallery',
            field=models.ManyToManyField(blank=True, to='hospital_blog.bloggallerymodel', verbose_name='گالری بلاگ'),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='short_desc_ar',
            field=models.TextField(max_length=500, verbose_name='متن کوتاه'),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='short_desc_en',
            field=models.TextField(max_length=500, verbose_name='متن کوتاه'),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='short_desc_fa',
            field=models.TextField(max_length=500, verbose_name='متن کوتاه'),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='short_desc_ru',
            field=models.TextField(max_length=500, verbose_name='متن کوتاه'),
        ),
    ]
