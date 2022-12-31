# Generated by Django 4.1.3 on 2022-12-31 13:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import extentions.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospital_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BenefactorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')),
                ('is_founder', models.BooleanField(default=False, verbose_name='بنیانگذار است؟')),
                ('about', models.TextField(verbose_name='درباره ی نیکوکار')),
            ],
            options={
                'verbose_name': 'خیر و نیکوکار',
                'verbose_name_plural': 'خیرین و نیکوکاران',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='BeneficiaryCommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوادگی')),
                ('desc', models.TextField(verbose_name='متن')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='بیوگرافی')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'نظر ذینفع',
                'verbose_name_plural': 'نظرات ذینفعان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CareersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=extentions.utils.career_code, max_length=20, verbose_name='کد موقعیت شغلی')),
                ('gender', models.CharField(choices=[('male', 'مرد'), ('female', 'زن')], max_length=7, verbose_name='جنسیت')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان موقعیت')),
                ('desc', models.TextField(verbose_name='توضیحات')),
                ('min_age', models.PositiveIntegerField(blank=True, null=True, verbose_name='حداقل سن')),
                ('max_age', models.PositiveIntegerField(blank=True, null=True, verbose_name='حداکثر سن')),
                ('image', models.ImageField(upload_to=extentions.utils.career_image_path, verbose_name='تصویر')),
                ('expriment', models.TextField(verbose_name='تجربه ی مورد نیاز')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال؟')),
            ],
            options={
                'verbose_name': 'موقعیت شغلی بیمارستان',
                'verbose_name_plural': 'موقعیت های شغلی بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ContactUsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='متن ارتباط')),
                ('name', models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')),
                ('email', models.EmailField(max_length=100, verbose_name='ایمیل کاربر')),
                ('phone', models.BigIntegerField(verbose_name='شماره تلفن')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان ارتباط')),
                ('is_read', models.BooleanField(default=False, verbose_name='بررسی شده یا نه')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'تماس مخاطب',
                'verbose_name_plural': 'تماس های مخاطبان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CriticismSuggestionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=extentions.utils.criticic_suggestion_code, max_length=20, verbose_name='کد پیگیری')),
                ('message', models.TextField(verbose_name='متن ارتباط')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام بیمار')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوادگی بیمار')),
                ('national_code', models.PositiveBigIntegerField(verbose_name='کدملی بیمار')),
                ('email', models.EmailField(max_length=100, verbose_name='ایمیل کاربر')),
                ('phone', models.BigIntegerField(verbose_name='شماره تلفن')),
                ('manager', models.CharField(max_length=100, verbose_name='نام مسیول')),
                ('is_read', models.BooleanField(default=False, verbose_name='بررسی شده یا نه')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'انتقاد و پیشنهاد مخاطب',
                'verbose_name_plural': 'انتقادات و پیشنهادات مخاطبان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='HireFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_checked', models.BooleanField(default=False, verbose_name='آیا بررسی شده است؟')),
                ('first_name', models.CharField(max_length=50, verbose_name='نام')),
                ('last_name', models.CharField(max_length=50, verbose_name='نام خانوادگی')),
                ('father', models.CharField(max_length=50, verbose_name='نام پدر')),
                ('national_code', models.CharField(max_length=10, unique=True, verbose_name='کدملی')),
                ('national_number', models.CharField(max_length=20, verbose_name='شماره شناسنامه')),
                ('burthday_date', models.DateField(verbose_name='تاریخ تولد')),
                ('burthday_place', models.CharField(max_length=100, verbose_name='محل تولد')),
                ('single_married', models.CharField(choices=[('single', 'مجرد'), ('married', 'متاهل')], max_length=10, verbose_name='وضعیت تاهل')),
                ('num_childs', models.PositiveIntegerField(default=0, verbose_name='تعداد فرزندان')),
                ('soldiering', models.CharField(choices=[('end', 'پایان خدمت'), ('abs_exemption', 'معافیت دایم'), ('edu_exemption', 'معافیت تحصیلی'), ('progressing', 'در حال انجام'), ('include', 'مشمول')], max_length=20, verbose_name='وضعیت نظام وظیفه')),
                ('end_date', models.DateField(verbose_name='تاریخ پایان طرح')),
                ('direct', models.CharField(max_length=100, verbose_name='معرف')),
                ('education', models.CharField(max_length=100, verbose_name='تحصیلات')),
                ('uni', models.CharField(max_length=100, verbose_name='نام دانشگاه')),
                ('address', models.TextField(verbose_name='آدرس محل زندگی')),
                ('phone', models.CharField(default=0, max_length=20, verbose_name='شماره تلفن')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('resume', models.FileField(upload_to=extentions.utils.resume_image_path, verbose_name='رزومه کاری مرتبط با کار درخواستی')),
            ],
            options={
                'verbose_name': 'فرم های استخدام',
                'verbose_name_plural': 'فرم های استخدام',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('description', models.CharField(max_length=500, verbose_name='متن')),
                ('is_from_boss', models.BooleanField(default=False, verbose_name='آیا این متن از سمت ریاست است؟')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان انتشار پست')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'اعلان',
                'verbose_name_plural': 'اعلانات',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='NotificationUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False, verbose_name='توسط کاربر خوانده شده؟')),
            ],
            options={
                'verbose_name': 'اعلان برای کاربر',
                'verbose_name_plural': 'اعلان برای کاربران',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PeopleAidModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')),
                ('email', models.EmailField(max_length=100, verbose_name='ایمیل کاربر')),
                ('phone', models.BigIntegerField(verbose_name='شماره تلفن')),
                ('price', models.PositiveBigIntegerField(verbose_name='مبلغ کمک شده')),
                ('date_of_aid', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ کمک')),
            ],
            options={
                'verbose_name': 'کمک مردمی',
                'verbose_name_plural': 'کمک های مردمی',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='WorkshopModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('length', models.CharField(max_length=50, verbose_name='طول دوره')),
                ('category', models.CharField(max_length=100, verbose_name='دسته بندی دوره')),
                ('capacity', models.PositiveIntegerField(verbose_name='ظرفیت دوره')),
                ('nums', models.PositiveIntegerField(verbose_name='تعداد شرکت کنندگان')),
                ('times', models.CharField(max_length=100, verbose_name='ساعات برگذاری')),
                ('proffessors', models.CharField(max_length=255, verbose_name='استادان دوره')),
                ('have_degree', models.BooleanField(default=False, verbose_name='آیا این دوره شامل مدرک میشود؟')),
                ('image', models.ImageField(upload_to=extentions.utils.workshop_image_path, verbose_name='تصویر')),
                ('start_date', models.DateField(verbose_name='تاریخ شروع دوره')),
            ],
            options={
                'verbose_name': 'کارگاه و دوره آموزشی',
                'verbose_name_plural': 'کارگاه ها و دوره های آموزشی',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PatientSightModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(verbose_name='متن')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_auth.patientmodel', verbose_name='بیمار')),
            ],
            options={
                'verbose_name': 'دیدگاه بیمار',
                'verbose_name_plural': 'دیدگاه بیماران',
                'ordering': ['-id'],
            },
        ),
    ]
