# Generated by Django 4.1.3 on 2022-12-18 16:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import extentions.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DegreeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='نوع مدرک')),
            ],
            options={
                'verbose_name': 'نوع مدرک',
                'verbose_name_plural': 'نوع مدرک ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DoctorInsuranceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance_exit', models.CharField(blank=True, max_length=50, null=True, verbose_name='بیمه ی غیر بیمارستان')),
            ],
            options={
                'verbose_name': 'بیمه ی پزشک',
                'verbose_name_plural': 'بیمه های پزشکان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DoctorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_code', models.CharField(max_length=15, verbose_name='کد نظام پزشکی')),
                ('position', models.TextField(blank=True, max_length=500, null=True, verbose_name='موقعیت')),
                ('bio', models.TextField(blank=True, max_length=500, null=True, verbose_name='بیوگرافی')),
                ('is_medicalteam', models.BooleanField(default=False, verbose_name='آیا این پزشک عضو تیم پزشکی است؟')),
                ('is_intenational', models.BooleanField(default=False, verbose_name='آیا این پزشک بین الملل است؟')),
                ('is_public', models.BooleanField(default=False, verbose_name='آیا این پزشک معمولی است؟')),
                ('is_clinic', models.BooleanField(default=False, verbose_name='آیا این پزشک درمانگاه است؟')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('degree', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_doctor.degreemodel', verbose_name='نوع مدرک')),
            ],
            options={
                'verbose_name': 'پزشک',
                'verbose_name_plural': 'پزشکان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='FamousPatientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوادگی')),
                ('profile', models.ImageField(upload_to=extentions.utils.famous_profile_image_path, verbose_name='تصویر')),
                ('desc', models.TextField(verbose_name='متن')),
            ],
            options={
                'verbose_name': 'چهره سرشناس مراجعه کننده',
                'verbose_name_plural': 'چهره های سرشناس مراجعه کننده',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TitleSkillModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان تخصص')),
            ],
            options={
                'verbose_name': 'عنوان تخصص',
                'verbose_name_plural': 'عناوین تخصص\u200cها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DoctorWorkTimeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('saturday', 'شنبه'), ('sunday', 'یک شنبه'), ('monday', 'دو شنبه'), ('tuesday', 'سه شنبه'), ('wednesday', 'چهار شنبه'), ('thursday', 'پنج شنبه'), ('friday', 'جمعه')], max_length=15, verbose_name='روز')),
                ('time_from', models.CharField(choices=[('6:00', '6:00'), ('6:30', '6:30'), ('7:00', '7:00'), ('7:30', '7:30'), ('8:00', '8:00'), ('8:30', '8:30'), ('9:00', '9:00'), ('9:30', '9:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'), ('21:00', '21:00'), ('21:30', '21:30'), ('22:00', '22:00'), ('22:30', '22:30'), ('23:00', '23:00'), ('23:30', '23:30'), ('24:00', '24:00')], max_length=15, verbose_name='از ساعت')),
                ('time_to', models.CharField(choices=[('6:00', '6:00'), ('6:30', '6:30'), ('7:00', '7:00'), ('7:30', '7:30'), ('8:00', '8:00'), ('8:30', '8:30'), ('9:00', '9:00'), ('9:30', '9:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'), ('21:00', '21:00'), ('21:30', '21:30'), ('22:00', '22:00'), ('22:30', '22:30'), ('23:00', '23:00'), ('23:30', '23:30'), ('24:00', '24:00')], max_length=15, verbose_name='تا ساعت')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_doctor.doctormodel', verbose_name='پزشک')),
            ],
            options={
                'verbose_name': 'زمان کاری پزشک',
                'verbose_name_plural': 'زمان\u200cهای کاری پزشکان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DoctorVacationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_time', models.DateField(default=django.utils.timezone.now, verbose_name='از تاریخ')),
                ('to_time', models.DateField(default=django.utils.timezone.now, verbose_name='تا تاریخ')),
                ('is_accepted', models.BooleanField(default=False, verbose_name='آیا تایید شده است؟')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_doctor.doctormodel', verbose_name='پزشک')),
            ],
            options={
                'verbose_name': 'زمان مرخصی پزشک',
                'verbose_name_plural': 'زمان\u200cهای مرخصی پزشکان',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='doctormodel',
            name='skill_title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_doctor.titleskillmodel', verbose_name='عنوان تخصص'),
        ),
    ]
