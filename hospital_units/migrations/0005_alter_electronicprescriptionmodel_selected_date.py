# Generated by Django 4.1.3 on 2023-01-05 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_units', '0004_remove_electronicprescriptionmodel_insurance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electronicprescriptionmodel',
            name='selected_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='زمان و تاریخ نوبت'),
        ),
    ]