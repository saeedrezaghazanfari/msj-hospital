# Generated by Django 4.1.3 on 2023-01-08 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital_contact', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationmodel',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='توسط کاربر خوانده شده؟'),
        ),
        migrations.AddField(
            model_name='notificationmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.DeleteModel(
            name='NotificationUserModel',
        ),
    ]
