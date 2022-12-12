# Generated by Django 4.1.3 on 2022-12-06 10:58

from django.db import migrations, models
import extentions.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AngiographyAngioplastyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'آنژیوگرافی و آنژیوپلاستی',
                'verbose_name_plural': 'آنژیوگرافی و آنژیوپلاستی ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ClinicModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'درمانگاه',
                'verbose_name_plural': 'درمانگاه ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DepartmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'دپارتمان',
                'verbose_name_plural': 'دپارتمان ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EmergencyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'اورژانس',
                'verbose_name_plural': 'اورژانس ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ImagingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'تصویربرداری',
                'verbose_name_plural': 'تصویربرداری ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='LaboratoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'آزمایشگاه',
                'verbose_name_plural': 'آزمایشگاه ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ParaclinicModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'پاراکلینیک',
                'verbose_name_plural': 'پاراکلینیک ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PharmacyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'داروخانه',
                'verbose_name_plural': 'داروخانه ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PhysiotherapyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'فیزیوتراپی',
                'verbose_name_plural': 'فیزیوتراپی ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SurgeryRoomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'اتاق عمل',
                'verbose_name_plural': 'اتاق های عمل',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TreatmentSectionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نام')),
                ('desc', models.TextField(verbose_name='متن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.units_image_path, verbose_name='تصویر')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('manager', models.CharField(blank=True, max_length=100, null=True, verbose_name='مدیر')),
            ],
            options={
                'verbose_name': 'بخش درمان',
                'verbose_name_plural': 'بخش های درمان',
                'ordering': ['-id'],
            },
        ),
    ]