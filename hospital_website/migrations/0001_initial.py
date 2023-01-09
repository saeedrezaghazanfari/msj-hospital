# Generated by Django 4.1.3 on 2023-01-09 21:07

from django.db import migrations, models
import extentions.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginCodePatientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=30, verbose_name='شماره تلفن')),
                ('code', models.IntegerField(default=extentions.utils.get_random_code, verbose_name='کد')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ تولید کد')),
                ('expire_date', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انقضای کد')),
                ('is_use', models.BooleanField(default=False, verbose_name='استفاده شده؟')),
                ('expire_mission', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انقضای عملیات')),
            ],
            options={
                'verbose_name': 'کد ارسال شده به شماره بیمار',
                'verbose_name_plural': 'کدهای ارسال شده به شماره بیماران ',
                'ordering': ['-id'],
            },
        ),
    ]
