# Generated by Django 4.1.3 on 2023-01-15 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_auth', '0002_remove_logincodemodel_usage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfullnamemodel',
            name='first_name_ar',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='userfullnamemodel',
            name='first_name_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='userfullnamemodel',
            name='first_name_fa',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='userfullnamemodel',
            name='first_name_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='userfullnamemodel',
            name='last_name_ar',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='userfullnamemodel',
            name='last_name_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='userfullnamemodel',
            name='last_name_fa',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='userfullnamemodel',
            name='last_name_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام خانوادگی'),
        ),
    ]