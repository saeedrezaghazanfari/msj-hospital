# Generated by Django 4.1.3 on 2023-04-16 15:07

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_contact', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopmodel',
            name='desc_ar',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات دوره'),
        ),
        migrations.AddField(
            model_name='workshopmodel',
            name='desc_en',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات دوره'),
        ),
        migrations.AddField(
            model_name='workshopmodel',
            name='desc_fa',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات دوره'),
        ),
        migrations.AddField(
            model_name='workshopmodel',
            name='desc_ru',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات دوره'),
        ),
    ]
