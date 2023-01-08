# Generated by Django 4.1.3 on 2023-01-06 21:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_doctor', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorvacationmodel',
            name='from_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='از تاریخ'),
        ),
        migrations.AddField(
            model_name='doctorvacationmodel',
            name='to_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='تا تاریخ'),
        ),
        migrations.AlterField(
            model_name='doctorvacationmodel',
            name='from_time',
            field=models.CharField(choices=[('6:00', '6:00'), ('6:30', '6:30'), ('7:00', '7:00'), ('7:30', '7:30'), ('8:00', '8:00'), ('8:30', '8:30'), ('9:00', '9:00'), ('9:30', '9:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'), ('21:00', '21:00'), ('21:30', '21:30'), ('22:00', '22:00'), ('22:30', '22:30'), ('23:00', '23:00'), ('23:30', '23:30'), ('24:00', '24:00')], default='9:00', max_length=15, verbose_name='از ساعت'),
        ),
        migrations.AlterField(
            model_name='doctorvacationmodel',
            name='to_time',
            field=models.CharField(choices=[('6:00', '6:00'), ('6:30', '6:30'), ('7:00', '7:00'), ('7:30', '7:30'), ('8:00', '8:00'), ('8:30', '8:30'), ('9:00', '9:00'), ('9:30', '9:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'), ('21:00', '21:00'), ('21:30', '21:30'), ('22:00', '22:00'), ('22:30', '22:30'), ('23:00', '23:00'), ('23:30', '23:30'), ('24:00', '24:00')], default='12:00', max_length=15, verbose_name='تا ساعت'),
        ),
    ]