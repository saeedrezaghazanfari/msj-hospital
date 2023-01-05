# Generated by Django 4.1.3 on 2023-01-04 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_units', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointmenttimemodel',
            options={'ordering': ['date'], 'verbose_name': 'زمان نوبتدهی', 'verbose_name_plural': 'زمان های نوبتدهی'},
        ),
        migrations.RemoveField(
            model_name='unitmodel',
            name='have_2_box',
        ),
        migrations.AddField(
            model_name='subunitmodel',
            name='have_2_box',
            field=models.BooleanField(default=False, verbose_name='آیا دو مرحله ای است؟'),
        ),
    ]