# Generated by Django 4.1.3 on 2022-12-14 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('workers', 'کارکنان'), ('it', 'واحد آی تی'), ('gaurd', 'حراست'), ('engineer', 'فنی'), ('aid', 'مددکاری'), ('official', 'اداری'), ('managering_group', 'هیات مدیره'), ('boss', 'ریاست'), ('management', 'مدیریت'), ('committe', 'کمیته ها')], max_length=20, verbose_name='نوع ارگان')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='نام')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, verbose_name='تلفن')),
                ('inside', models.PositiveIntegerField(blank=True, null=True, verbose_name='داخلی')),
                ('address', models.CharField(max_length=255, verbose_name='آدرس')),
            ],
            options={
                'verbose_name': 'ارگان',
                'verbose_name_plural': 'ارگان ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='OrganItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='نام')),
                ('last_name', models.CharField(max_length=50, verbose_name='نام خانوادگی')),
                ('national_code', models.CharField(max_length=10, unique=True, verbose_name='کدملی')),
                ('phone', models.CharField(default=0, max_length=20, verbose_name='شماره تلفن')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('job', models.CharField(max_length=50, verbose_name='سمت')),
                ('address', models.CharField(max_length=255, verbose_name='آدرس')),
                ('organ', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_official.organmodel', verbose_name='ارگان')),
            ],
            options={
                'verbose_name': 'عضو ارگان',
                'verbose_name_plural': 'اعضای ارگان',
                'ordering': ['-id'],
            },
        ),
    ]
