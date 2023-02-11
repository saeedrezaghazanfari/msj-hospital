# Generated by Django 4.1.3 on 2023-02-06 13:51

from django.db import migrations, models
import extentions.utils


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_ipd', '0002_remove_ipdcodemodel_ipd_ipdcodemodel_expire_mission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipdmodel',
            name='code',
            field=models.IntegerField(default=extentions.utils.get_patient_tracking_code, null=True, verbose_name='کد'),
        ),
        migrations.AlterField(
            model_name='ipdmodel',
            name='username',
            field=models.CharField(max_length=10, verbose_name='شماره پاسپورت / کدملی'),
        ),
    ]