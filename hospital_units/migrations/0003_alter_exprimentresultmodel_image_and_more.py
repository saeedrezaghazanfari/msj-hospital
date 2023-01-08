# Generated by Django 4.1.3 on 2023-01-06 20:35

from django.db import migrations, models
import extentions.utils


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_units', '0002_rename_is_show_send_sms_exprimentresultmodel_is_sent_sms_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exprimentresultmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=extentions.utils.experiment_result_image_path, verbose_name='تصویر آزمایش'),
        ),
        migrations.AlterField(
            model_name='exprimentresultmodel',
            name='result',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='جواب آزمایش'),
        ),
    ]