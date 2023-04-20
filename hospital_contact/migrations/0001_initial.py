# Generated by Django 4.1.3 on 2023-04-20 19:18

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import hospital_extentions.utils
import uuid


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
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی')),
                ('is_founder', models.BooleanField(default=False, verbose_name='بنیانگذار است؟')),
                ('about_fa', ckeditor.fields.RichTextField(verbose_name='درباره\u200cی نیکوکار')),
                ('about_en', ckeditor.fields.RichTextField(verbose_name='درباره\u200cی نیکوکار')),
                ('about_ar', ckeditor.fields.RichTextField(verbose_name='درباره\u200cی نیکوکار')),
                ('about_ru', ckeditor.fields.RichTextField(verbose_name='درباره\u200cی نیکوکار')),
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
                ('first_name_fa', models.CharField(max_length=100, verbose_name='نام')),
                ('first_name_en', models.CharField(max_length=100, verbose_name='نام')),
                ('first_name_ar', models.CharField(max_length=100, verbose_name='نام')),
                ('first_name_ru', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name_fa', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی')),
                ('last_name_en', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی')),
                ('last_name_ar', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی')),
                ('last_name_ru', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی')),
                ('desc_fa', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_en', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_ar', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_ru', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('bio_fa', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='بیوگرافی')),
                ('bio_en', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='بیوگرافی')),
                ('bio_ar', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='بیوگرافی')),
                ('bio_ru', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='بیوگرافی')),
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
                ('code', models.CharField(default=hospital_extentions.utils.career_code, max_length=20, verbose_name='کد موقعیت شغلی')),
                ('gender', models.CharField(choices=[('male', 'مرد'), ('female', 'زن')], max_length=7, verbose_name='جنسیت')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان موقعیت')),
                ('desc', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('min_age', models.PositiveIntegerField(blank=True, null=True, verbose_name='حداقل سن')),
                ('max_age', models.PositiveIntegerField(blank=True, null=True, verbose_name='حداکثر سن')),
                ('image', models.ImageField(blank=True, null=True, upload_to=hospital_extentions.utils.career_image_path, verbose_name='تصویر')),
                ('expriment', ckeditor.fields.RichTextField(verbose_name='تجربه ی مورد نیاز')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال؟')),
            ],
            options={
                'verbose_name': 'موقعیت شغلی بیمارستان',
                'verbose_name_plural': 'موقعیت\u200cهای شغلی بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ContactUsModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('message', ckeditor.fields.RichTextField(verbose_name='متن ارتباط')),
                ('name', models.CharField(max_length=100, verbose_name='نام و نام\u200cخانوادگی')),
                ('email', models.EmailField(max_length=100, verbose_name='ایمیل کاربر')),
                ('phone', models.BigIntegerField(verbose_name='شماره تلفن')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان ارتباط')),
                ('is_read', models.BooleanField(default=False, verbose_name='بررسی شده یا نه')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'تماس مخاطب',
                'verbose_name_plural': 'تماس\u200cهای مخاطبان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CriticismSuggestionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=hospital_extentions.utils.criticic_suggestion_code, max_length=20, verbose_name='کد پیگیری')),
                ('message', ckeditor.fields.RichTextField(verbose_name='متن ارتباط')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام بیمار')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی بیمار')),
                ('national_code', models.PositiveBigIntegerField(verbose_name='کدملی بیمار')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='ایمیل کاربر')),
                ('phone', models.BigIntegerField(verbose_name='شماره تلفن')),
                ('manager', models.CharField(max_length=100, verbose_name='نام مسئول')),
                ('is_read', models.BooleanField(default=False, verbose_name='بررسی\u200cشده یا نه')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'انتقاد و پیشنهاد مخاطب',
                'verbose_name_plural': 'انتقادات و پیشنهادات مخاطبان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='FamousPatientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name_fa', models.CharField(max_length=100, verbose_name='نام')),
                ('first_name_en', models.CharField(max_length=100, verbose_name='نام')),
                ('first_name_ar', models.CharField(max_length=100, verbose_name='نام')),
                ('first_name_ru', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name_fa', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی')),
                ('last_name_en', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی')),
                ('last_name_ar', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی')),
                ('last_name_ru', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی')),
                ('profile', models.ImageField(upload_to=hospital_extentions.utils.famous_profile_image_path, verbose_name='تصویر')),
                ('desc_fa', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_en', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_ar', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_ru', ckeditor.fields.RichTextField(verbose_name='متن')),
            ],
            options={
                'verbose_name': 'چهره سرشناس مراجعه کننده',
                'verbose_name_plural': 'چهره\u200cهای سرشناس مراجعه کننده',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='HireFormModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_checked', models.BooleanField(default=False, verbose_name='آیا بررسی\u200cشده است؟')),
                ('first_name', models.CharField(max_length=50, verbose_name='نام')),
                ('last_name', models.CharField(max_length=50, verbose_name='نام\u200cخانوادگی')),
                ('father', models.CharField(max_length=50, verbose_name='نام پدر')),
                ('national_code', models.CharField(max_length=10, verbose_name='کدملی')),
                ('national_number', models.CharField(max_length=20, verbose_name='شماره شناسنامه')),
                ('birthday_date', models.DateField(verbose_name='تاریخ تولد')),
                ('birthday_place', models.CharField(max_length=100, verbose_name='محل تولد')),
                ('single_married', models.CharField(choices=[('single', 'مجرد'), ('married', 'متاهل')], max_length=10, verbose_name='وضعیت تاهل')),
                ('num_childs', models.PositiveIntegerField(default=0, verbose_name='تعداد فرزندان')),
                ('soldiering', models.CharField(choices=[('end', 'پایان خدمت'), ('abs_exemption', 'معافیت دائم'), ('edu_exemption', 'معافیت تحصیلی'), ('progressing', 'در حال انجام'), ('include', 'مشمول')], max_length=20, verbose_name='وضعیت نظام\u200cوظیفه')),
                ('end_date', models.DateField(verbose_name='تاریخ پایان طرح')),
                ('direct', models.CharField(max_length=100, verbose_name='معرف')),
                ('education', models.CharField(max_length=100, verbose_name='تحصیلات')),
                ('uni', models.CharField(max_length=100, verbose_name='نام دانشگاه')),
                ('address', models.TextField(verbose_name='آدرس محل\u200cزندگی')),
                ('phone', models.CharField(default=0, max_length=20, verbose_name='شماره تلفن')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('resume', models.FileField(upload_to=hospital_extentions.utils.resume_image_path, verbose_name='رزومه کاری مرتبط با کار درخواستی')),
            ],
            options={
                'verbose_name': 'فرم استخدام',
                'verbose_name_plural': 'فرم\u200cهای استخدام',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('description', ckeditor.fields.RichTextField(max_length=500, verbose_name='متن')),
                ('is_from_boss', models.BooleanField(default=False, verbose_name='آیا این متن از سمت ریاست است؟')),
                ('is_published', models.BooleanField(default=False, verbose_name='منتشر شود؟')),
                ('is_read', models.BooleanField(default=False, verbose_name='توسط کاربر خوانده شده؟')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'اعلان',
                'verbose_name_plural': 'اعلانات',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PeopleAidModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام\u200cخانوادگی')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='ایمیل')),
                ('phone', models.BigIntegerField(blank=True, null=True, verbose_name='شماره تلفن')),
                ('price', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='مبلغ کمک شده')),
                ('date_of_aid', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ کمک')),
            ],
            options={
                'verbose_name': 'کمک مردمی',
                'verbose_name_plural': 'کمک\u200cهای مردمی',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='WorkshopModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=50, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=50, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=50, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=50, verbose_name='عنوان')),
                ('desc_fa', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات دوره')),
                ('desc_en', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات دوره')),
                ('desc_ar', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات دوره')),
                ('desc_ru', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات دوره')),
                ('length', models.CharField(max_length=50, verbose_name='طول دوره')),
                ('category_fa', models.CharField(max_length=100, verbose_name='دسته\u200cبندی دوره')),
                ('category_en', models.CharField(max_length=100, verbose_name='دسته\u200cبندی دوره')),
                ('category_ar', models.CharField(max_length=100, verbose_name='دسته\u200cبندی دوره')),
                ('category_ru', models.CharField(max_length=100, verbose_name='دسته\u200cبندی دوره')),
                ('capacity', models.PositiveIntegerField(verbose_name='ظرفیت دوره')),
                ('times', models.CharField(max_length=100, verbose_name='ساعات برگذاری')),
                ('proffessors_fa', models.CharField(max_length=255, verbose_name='استادان دوره')),
                ('proffessors_en', models.CharField(max_length=255, verbose_name='استادان دوره')),
                ('proffessors_ar', models.CharField(max_length=255, verbose_name='استادان دوره')),
                ('proffessors_ru', models.CharField(max_length=255, verbose_name='استادان دوره')),
                ('have_degree', models.BooleanField(default=False, verbose_name='آیا این دوره شامل مدرک میشود؟')),
                ('image', models.ImageField(upload_to=hospital_extentions.utils.workshop_image_path, verbose_name='تصویر')),
                ('start_date', models.DateField(verbose_name='تاریخ شروع دوره')),
            ],
            options={
                'verbose_name': 'کارگاه و دوره آموزشی',
                'verbose_name_plural': 'کارگاه\u200cها و دوره\u200cهای آموزشی',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PatientSightModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc_fa', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_en', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_ar', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_ru', ckeditor.fields.RichTextField(verbose_name='متن')),
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
