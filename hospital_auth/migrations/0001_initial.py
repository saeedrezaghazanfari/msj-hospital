# Generated by Django 4.1.3 on 2022-12-06 10:58

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import extentions.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=10, unique=True, verbose_name='کدملی')),
                ('phone', models.CharField(default=0, max_length=20, verbose_name='شماره تلفن')),
                ('fixed_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='تلفن ثابت')),
                ('gender', models.CharField(choices=[('male', 'مرد'), ('female', 'زن')], max_length=7, verbose_name='جنسیت')),
                ('profile', models.ImageField(blank=True, null=True, upload_to=extentions.utils.profile_image_path, verbose_name='پروفایل')),
                ('wallet_balance', models.FloatField(default=0, verbose_name='موجودی کیف پول')),
                ('is_send_sms', models.BooleanField(default=False, verbose_name='آیا پیامک های پزشکی ارسال شود؟')),
                ('is_active2', models.BooleanField(default=False, help_text='اگر اطلاعات حساب کاربر کامل بود آنگاه این گزینه فعال میشود.', verbose_name='فعال بودن حساب جهت استفاده از اپلیکیشن')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SupporterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پشتیبان',
                'verbose_name_plural': 'پشتیبانان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='LoginCodeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(default=extentions.utils.get_random_code, verbose_name='کد')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ تولید کد')),
                ('expire_date', models.DateTimeField(blank=True, help_text='این فیلد لازم نیست پر شود. بعد از ثبت رکورد بصورت اتوماتیک ثبت میشود.', null=True, verbose_name='تاریخ انقضای کد')),
                ('is_use', models.BooleanField(default=False, verbose_name='استفاده شده؟')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'کد ورود به حساب کاربری',
                'verbose_name_plural': 'کدهای ورود به حساب های کاربری',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ContentProducerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تولیدکننده ی محتوا',
                'verbose_name_plural': 'تولیدکنندگان محتوا',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='AdmissionsAdminModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'ادمین پذیرش',
                'verbose_name_plural': 'ادمین های پذیرش',
                'ordering': ['-id'],
            },
        ),
    ]
