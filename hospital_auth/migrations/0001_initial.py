# Generated by Django 4.1.3 on 2022-12-31 13:23

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
                ('gender', models.CharField(choices=[('male', 'مرد'), ('female', 'زن')], default='male', max_length=7, verbose_name='جنسیت')),
                ('age', models.PositiveIntegerField(blank=True, null=True, verbose_name='سن')),
                ('profile', models.ImageField(blank=True, null=True, upload_to=extentions.utils.profile_image_path, verbose_name='پروفایل')),
                ('is_doctor_manager', models.BooleanField(default=False, verbose_name='نمایش پنل پزشکی')),
                ('is_newsletter_manager', models.BooleanField(default=False, verbose_name='قابلیت ارسال خبرنامه')),
                ('is_blog_manager', models.BooleanField(default=False, verbose_name='قابلیت پست گذاشتن')),
                ('is_news_manager', models.BooleanField(default=False, verbose_name='قابلیت خبر گذاشتن')),
                ('is_note_manager', models.BooleanField(default=False, verbose_name='قابلیت نوشتن نوت پزشکی')),
                ('is_expriment_manager', models.BooleanField(default=False, verbose_name='قابلیت گذاشتن جواب آزمایش و تصویربرداری های بیمار')),
                ('is_appointment_manager', models.BooleanField(default=False, verbose_name='قابلیت دسترسی به نوبت دهی آنلاین')),
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
            name='IPDModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, unique=True, verbose_name='شماره پاسپورت / کدملی')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوادگی')),
                ('phone', models.CharField(default=0, max_length=20, verbose_name='شماره تلفن')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('gender', models.CharField(choices=[('male', 'مرد'), ('female', 'زن')], default='male', max_length=7, verbose_name='جنسیت')),
                ('age', models.PositiveIntegerField(blank=True, null=True, verbose_name='سن')),
                ('description', models.TextField(verbose_name='شرح بیماری')),
                ('document', models.ImageField(blank=True, null=True, upload_to=extentions.utils.ipd_doc_image_path, verbose_name='مستندات')),
                ('country', models.CharField(max_length=100, verbose_name='کشور')),
                ('city', models.CharField(max_length=100, verbose_name='شهر')),
                ('is_answered', models.BooleanField(default=False, verbose_name='آیا جواب داده شده است؟')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'بیمار بین الملل',
                'verbose_name_plural': 'بیماران بین الملل',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PatientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, unique=True, verbose_name='کدملی')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوادگی')),
                ('phone', models.CharField(default=0, max_length=20, verbose_name='شماره تلفن')),
                ('gender', models.CharField(choices=[('male', 'مرد'), ('female', 'زن')], default='male', max_length=7, verbose_name='جنسیت')),
                ('age', models.PositiveIntegerField(verbose_name='سن')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'بیمار',
                'verbose_name_plural': 'بیماران',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='LoginCodeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(default=extentions.utils.get_random_code, verbose_name='کد')),
                ('code_login', models.CharField(default=extentions.utils.get_links_code, editable=False, max_length=30, verbose_name='کد ورود')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ تولید کد')),
                ('expire_date', models.DateTimeField(blank=True, help_text='این فیلد لازم نیست پر شود. بعد از ثبت رکورد بصورت اتوماتیک ثبت میشود.', null=True, verbose_name='تاریخ انقضای کد')),
                ('usage', models.CharField(blank=True, choices=[('login', 'ورود کاربر به پنل')], max_length=20, null=True, verbose_name='عنوان استفاده ی کد')),
                ('is_use', models.BooleanField(default=False, verbose_name='استفاده شده؟')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'کد ورود به حساب کاربری',
                'verbose_name_plural': 'کدهای ورود به حساب های کاربری',
                'ordering': ['-id'],
            },
        ),
    ]
