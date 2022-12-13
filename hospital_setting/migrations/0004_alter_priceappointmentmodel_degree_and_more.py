# Generated by Django 4.1.3 on 2022-12-13 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_doctor', '0003_alter_doctormodel_degree_and_more'),
        ('hospital_setting', '0003_alter_pricebedmodel_insurance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priceappointmentmodel',
            name='degree',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_doctor.degreemodel', verbose_name='نوع مدرک'),
        ),
        migrations.AlterField(
            model_name='priceappointmentmodel',
            name='insurance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_setting.insurancemodel', verbose_name='بیمه'),
        ),
        migrations.AlterField(
            model_name='priceappointmentmodel',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_doctor.titleskillmodel', verbose_name='عنوان تخصص'),
        ),
        migrations.AlterField(
            model_name='pricesurgraymodel',
            name='insurance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_setting.insurancemodel', verbose_name='بیمه'),
        ),
    ]
