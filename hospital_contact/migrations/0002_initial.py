# Generated by Django 4.1.3 on 2022-12-14 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospital_contact', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital_units', '0001_initial'),
        ('hospital_doctor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientsightmodel',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_units.unitmodel', verbose_name='بخش'),
        ),
        migrations.AddField(
            model_name='notificationusermodel',
            name='notification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_contact.notificationmodel', verbose_name='اعلان'),
        ),
        migrations.AddField(
            model_name='notificationusermodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='hireformmodel',
            name='career',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_contact.careersmodel', verbose_name='موقعیت شغلی'),
        ),
        migrations.AddField(
            model_name='hireformmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='criticismsuggestionmodel',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_units.unitmodel', verbose_name='نام بخش'),
        ),
        migrations.AddField(
            model_name='careersmodel',
            name='degree',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_doctor.degreemodel', verbose_name='نوع مدرک'),
        ),
        migrations.AddField(
            model_name='careersmodel',
            name='skill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_doctor.titleskillmodel', verbose_name='تخصص'),
        ),
        migrations.AddField(
            model_name='careersmodel',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_units.unitmodel', verbose_name='بخش مربوطه'),
        ),
    ]
