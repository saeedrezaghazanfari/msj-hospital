# Generated by Django 4.1.3 on 2023-04-15 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_setting', '0002_settingmodel_fax_settingmodel_telegram'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settingmodel',
            name='facs',
        ),
    ]
