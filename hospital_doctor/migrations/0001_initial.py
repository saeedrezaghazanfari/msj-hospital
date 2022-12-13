# Generated by Django 4.1.3 on 2022-12-13 12:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
            name='DoctorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_code', models.BigIntegerField(verbose_name='کد نظام پزشکی')),
                ('position', models.TextField(blank=True, max_length=500, null=True, verbose_name='موقعیت')),
                ('bio', models.TextField(blank=True, max_length=500, null=True, verbose_name='بیوگرافی')),
                ('is_intenational', models.BooleanField(default=False, verbose_name='آیا این پزشک بین الملل است؟')),
                ('is_medicalteam', models.BooleanField(default=False, verbose_name='آیا این پزشک عضو تیم پزشکی است؟')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_doctor.degreemodel', verbose_name='نوع مدرک')),
            ],
            options={
                'verbose_name': 'پزشک',
                'verbose_name_plural': 'پزشکان',
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
                ('time', models.CharField(choices=[('6-7', '6-7'), ('7-8', '7-8'), ('8-9', '8-9'), ('9-10', '9-10'), ('10-11', '10-11'), ('11-12', '11-12'), ('12-13', '12-13'), ('13-14', '13-14'), ('14-15', '14-15'), ('15-16', '15-16'), ('16-17', '16-17'), ('17-18', '17-18'), ('18-19', '18-19'), ('19-20', '19-20'), ('20-21', '20-21'), ('21-22', '21-22'), ('22-23', '22-23'), ('23-24', '23-24')], max_length=15, verbose_name='بازه ی زمانی')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_doctor.doctormodel', verbose_name='پزشک')),
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
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_doctor.doctormodel', verbose_name='پزشک')),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_doctor.titleskillmodel', verbose_name='عنوان تخصص'),
        ),
    ]
