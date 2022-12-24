# Generated by Django 4.1.3 on 2022-12-24 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital_doctor', '0001_initial'),
        ('hospital_setting', '0001_initial'),
        ('hospital_units', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctormodel',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_units.unitmodel', verbose_name='بخش'),
        ),
        migrations.AddField(
            model_name='doctormodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='doctorinsurancemodel',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_doctor.doctormodel', verbose_name='پزشک'),
        ),
        migrations.AddField(
            model_name='doctorinsurancemodel',
            name='insurance_hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_setting.insurancemodel', verbose_name='بیمه ی طرف بیمارستان'),
        ),
    ]
