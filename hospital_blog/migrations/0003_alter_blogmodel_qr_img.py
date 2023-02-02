# Generated by Django 4.1.3 on 2023-02-01 10:50

from django.db import migrations, models
import extentions.utils


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_blog', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='qr_img',
            field=models.ImageField(blank=True, editable=False, null=True, upload_to=extentions.utils.blog_qrcode_image_path, verbose_name='تصویر کد QR'),
        ),
    ]