# Generated by Django 4.1.3 on 2022-12-24 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_setting', '0002_remove_priceappointmentmodel_price_free_and_more'),
        ('hospital_doctor', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctormodel',
            name='isinstances',
            field=models.ManyToManyField(to='hospital_setting.insurancemodel', verbose_name='بیمه ها'),
        ),
        migrations.DeleteModel(
            name='DoctorInsuranceModel',
        ),
    ]