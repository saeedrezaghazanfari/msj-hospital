# Generated by Django 4.1.3 on 2023-01-24 13:53

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import extentions.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospital_doctor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=255, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=255, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=255, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=255, verbose_name='عنوان')),
                ('description_fa', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('description_en', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('description_ar', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('description_ru', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('image', models.ImageField(upload_to=extentions.utils.certificate_image_path, verbose_name='تصویر')),
                ('year_certif', models.IntegerField(verbose_name='سال اخذ')),
                ('year_expire', models.IntegerField(verbose_name='تاریخ اعتبار')),
            ],
            options={
                'verbose_name': 'گواهینامه',
                'verbose_name_plural': 'گواهینامه ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ContactInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=500, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=500, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=500, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=500, verbose_name='عنوان')),
                ('phones', models.CharField(max_length=100, verbose_name='تلفن ها')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
            ],
            options={
                'verbose_name': 'اطلاعات تماس',
                'verbose_name_plural': 'اطلاعات تماس',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=100, verbose_name='عنوان')),
                ('image', models.ImageField(upload_to=extentions.utils.costs_image_path, verbose_name='تصویر')),
                ('year', models.PositiveIntegerField(verbose_name='سال')),
            ],
            options={
                'verbose_name': 'ارزش بیمارستان',
                'verbose_name_plural': 'ارزش های بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='FAQModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_fa', models.TextField(verbose_name='پرسش')),
                ('question_en', models.TextField(verbose_name='پرسش')),
                ('question_ar', models.TextField(verbose_name='پرسش')),
                ('question_ru', models.TextField(verbose_name='پرسش')),
                ('answer_fa', models.TextField(verbose_name='پاسخ')),
                ('answer_en', models.TextField(verbose_name='پاسخ')),
                ('answer_ar', models.TextField(verbose_name='پاسخ')),
                ('answer_ru', models.TextField(verbose_name='پاسخ')),
            ],
            options={
                'verbose_name': 'سوال پر تکرار',
                'verbose_name_plural': 'سوالات پر تکرار',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='HomeGalleryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=255, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=255, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=255, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=255, verbose_name='عنوان')),
                ('image', models.ImageField(upload_to=extentions.utils.home_gallery_image_path, verbose_name='تصویر')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'آیتم گالری صفحه ی خانه',
                'verbose_name_plural': 'آیتم های گالری صفحه ی خانه',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='HospitalFacilityModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=100, verbose_name='عنوان')),
                ('image', models.ImageField(upload_to=extentions.utils.facility_image_path, verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'امکانات بیمارستان',
                'verbose_name_plural': 'امکانات های بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='HospitalGalleryItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('file_type', models.CharField(choices=[('video', 'ویدیو'), ('image', 'تصویر')], max_length=20, verbose_name='نوع فایل')),
                ('file', models.ImageField(blank=True, help_text='اگر فایل شما تصویر میباشد تصویر مورد نظر را وارد کنید.', null=True, upload_to=extentions.utils.gallery_image_path, verbose_name='فایل')),
                ('file_link', models.CharField(blank=True, help_text='اگر فایل شما ویدیو میباشد لینک فیلم را وارد کنید.', max_length=255, null=True, verbose_name='لینک فایل')),
            ],
            options={
                'verbose_name': 'آیتم گالری',
                'verbose_name_plural': 'آیتم های گالری',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='HospitalPoliticModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=100, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': 'سیاست بیمارستان',
                'verbose_name_plural': 'سیاست های بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='InsuranceModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=100, verbose_name='نام بیمه')),
                ('img', models.ImageField(upload_to=extentions.utils.insurance_image_path, verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'بیمه طرف قرارداد',
                'verbose_name_plural': 'بیمه های طرف قرارداد',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='NewsLetterEmailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, verbose_name='ایمیل')),
            ],
            options={
                'verbose_name': 'ایمیل خبرنامه',
                'verbose_name_plural': 'ایمیل های خبرنامه',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PriceServiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=200, verbose_name='عنوان')),
                ('desc_fa', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_en', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_ar', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_ru', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('price_special', models.PositiveBigIntegerField(verbose_name='مبلغ خصوصی')),
                ('price_govern', models.PositiveBigIntegerField(verbose_name='مبلغ دولتی')),
                ('diffrence', models.PositiveBigIntegerField(verbose_name='تفاوت')),
                ('year', models.IntegerField(verbose_name='سال تعرفه')),
            ],
            options={
                'verbose_name': 'تعرفه خدمات بیمارستان',
                'verbose_name_plural': 'تعرفه خدمات بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ReportModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_bound', models.CharField(max_length=100, verbose_name='مدت عملکرد')),
                ('description_fa', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('description_en', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('description_ar', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('description_ru', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extentions.utils.report_image_path, verbose_name='تصویر')),
                ('video_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='لینک ویدیو')),
            ],
            options={
                'verbose_name': 'گزارش عملکرد بیمارستان',
                'verbose_name_plural': 'گزارش عملکرد های بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ResultModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=100, verbose_name='عنوان')),
                ('desc_fa', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_en', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_ar', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('desc_ru', ckeditor.fields.RichTextField(verbose_name='متن')),
            ],
            options={
                'verbose_name': 'دستاورد بیمارستان',
                'verbose_name_plural': 'دستاورد های بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SettingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_scale', models.FloatField(blank=True, null=True, verbose_name='مقیاس ایکس')),
                ('y_scale', models.FloatField(blank=True, null=True, verbose_name='مقیاس ایگرگ')),
                ('marker_text_fa', models.CharField(blank=True, max_length=50, null=True, verbose_name='متن شما روی نقشه')),
                ('marker_text_en', models.CharField(blank=True, max_length=50, null=True, verbose_name='متن شما روی نقشه')),
                ('marker_text_ar', models.CharField(blank=True, max_length=50, null=True, verbose_name='متن شما روی نقشه')),
                ('marker_text_ru', models.CharField(blank=True, max_length=50, null=True, verbose_name='متن شما روی نقشه')),
                ('address_fa', models.CharField(max_length=255, verbose_name='آدرس')),
                ('address_en', models.CharField(max_length=255, verbose_name='آدرس')),
                ('address_ar', models.CharField(max_length=255, verbose_name='آدرس')),
                ('address_ru', models.CharField(max_length=255, verbose_name='آدرس')),
                ('email', models.EmailField(max_length=255, verbose_name='ایمیل')),
                ('phone', models.CharField(max_length=255, verbose_name='تلفن')),
                ('facs', models.CharField(max_length=255, verbose_name='فکس')),
                ('from_to_fa', models.CharField(max_length=200, verbose_name='زمان گشایش')),
                ('from_to_en', models.CharField(max_length=200, verbose_name='زمان گشایش')),
                ('from_to_ar', models.CharField(max_length=200, verbose_name='زمان گشایش')),
                ('from_to_ru', models.CharField(max_length=200, verbose_name='زمان گشایش')),
                ('history_fa', ckeditor.fields.RichTextField(verbose_name='تاریخچه')),
                ('history_en', ckeditor.fields.RichTextField(verbose_name='تاریخچه')),
                ('history_ar', ckeditor.fields.RichTextField(verbose_name='تاریخچه')),
                ('history_ru', ckeditor.fields.RichTextField(verbose_name='تاریخچه')),
                ('aparat', models.CharField(blank=True, max_length=100, null=True, verbose_name='آپارات')),
                ('linkedin', models.CharField(blank=True, max_length=100, null=True, verbose_name='لینکدین')),
                ('facebook', models.CharField(blank=True, max_length=100, null=True, verbose_name='فیسبوک')),
                ('twitter', models.CharField(blank=True, max_length=100, null=True, verbose_name='توییتر')),
                ('instagram', models.CharField(blank=True, max_length=100, null=True, verbose_name='اینستاگرام')),
                ('whatsapp', models.CharField(blank=True, max_length=100, null=True, verbose_name='واتساپ')),
                ('bank_name_fa', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام بانک')),
                ('bank_name_en', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام بانک')),
                ('bank_name_ar', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام بانک')),
                ('bank_name_ru', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام بانک')),
                ('bank_account_owner_fa', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام صاحب حساب')),
                ('bank_account_owner_en', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام صاحب حساب')),
                ('bank_account_owner_ar', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام صاحب حساب')),
                ('bank_account_owner_ru', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام صاحب حساب')),
                ('bank_account_cardnum', models.CharField(blank=True, max_length=100, null=True, verbose_name='شماره کارت')),
                ('bank_account_num', models.CharField(blank=True, max_length=100, null=True, verbose_name='شماره حساب')),
                ('bank_account_shabanum', models.CharField(blank=True, max_length=100, null=True, verbose_name='شماره شبا')),
                ('have_signup_page', models.BooleanField(default=False, verbose_name='صفحه ثبتنام کاربران نمایش داده شود؟')),
            ],
            options={
                'verbose_name': '\u200cتنظیمات',
                'verbose_name_plural': '\u200cتنظیمات',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PriceSurgrayModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=200, verbose_name='عنوان')),
                ('price_free', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='مبلغ آزاد')),
                ('price_insurance', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='مبلغ بیمه')),
                ('year', models.IntegerField(verbose_name='سال تعرفه')),
                ('insurance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_setting.insurancemodel', verbose_name='بیمه')),
            ],
            options={
                'verbose_name': 'تعرفه عمل جراحی بیمارستان',
                'verbose_name_plural': 'تعرفه عمل جراحی های بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PriceBedModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=200, verbose_name='عنوان')),
                ('price_free', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='مبلغ آزاد')),
                ('price_insurance', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='مبلغ بیمه')),
                ('year', models.IntegerField(verbose_name='سال تعرفه')),
                ('insurance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_setting.insurancemodel', verbose_name='بیمه')),
            ],
            options={
                'verbose_name': 'تعرفه تخت بیمارستان',
                'verbose_name_plural': 'تعرفه تخت های بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PriceAppointmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveBigIntegerField(default=0, verbose_name='مبلغ')),
                ('degree', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_doctor.degreemodel', verbose_name='نوع مدرک')),
                ('insurance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital_setting.insurancemodel', verbose_name='بیمه')),
            ],
            options={
                'verbose_name': 'تعرفه ی نوبت دهی',
                'verbose_name_plural': 'تعرفه ی نوبت دهی ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='HospitalGalleryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=100, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=100, verbose_name='عنوان')),
                ('items', models.ManyToManyField(to='hospital_setting.hospitalgalleryitemmodel', verbose_name='آیتم/آیتم ها')),
            ],
            options={
                'verbose_name': 'گالری بیمارستان',
                'verbose_name_plural': 'گالری های بیمارستان',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='AncientsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_en', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_ar', models.CharField(max_length=200, verbose_name='عنوان')),
                ('title_ru', models.CharField(max_length=200, verbose_name='عنوان')),
                ('image', models.ImageField(upload_to=extentions.utils.ancient_image_path, verbose_name='تصویر')),
                ('full_name_fa', models.CharField(max_length=255, verbose_name='نام پزشک مرحوم')),
                ('full_name_en', models.CharField(max_length=255, verbose_name='نام پزشک مرحوم')),
                ('full_name_ar', models.CharField(max_length=255, verbose_name='نام پزشک مرحوم')),
                ('full_name_ru', models.CharField(max_length=255, verbose_name='نام پزشک مرحوم')),
                ('description_fa', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('description_en', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('description_ar', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('description_ru', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('video_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='لینک ویدیو')),
                ('gallery', models.ManyToManyField(to='hospital_setting.hospitalgalleryitemmodel', verbose_name='گالری')),
            ],
            options={
                'verbose_name': 'گذشتگان بیمارستان',
                'verbose_name_plural': 'گذشتگان بیمارستان',
                'ordering': ['-id'],
            },
        ),
    ]
