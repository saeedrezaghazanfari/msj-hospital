# Generated by Django 4.1.3 on 2022-12-25 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logincodepatientmodel',
            name='usage',
        ),
    ]
