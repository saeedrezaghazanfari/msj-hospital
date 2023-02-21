import datetime
from django import forms
from hospital_auth.models import User, PatientModel
from django.utils.translation import gettext_lazy as _
from hospital_setting.models import InsuranceModel
from hospital_doctor.models import (
    DoctorModel, TitleSkillModel, DegreeModel, 
    DoctorVacationModel, DoctorWorkTimeModel
)
from hospital_units.models import (
    UnitModel, AppointmentTimeModel, LimitTurnTimeModel, AppointmentTipModel, 
    AppointmentTipSMSModel, SubUnitModel, ElectronicPrescriptionModel, ExprimentResultModel
)
from hospital_blog.models import (
    BlogModel, TagModel, CategoryModel, BlogGalleryModel, MedicalNoteModel, SMSTextModel, PampheletModel
)
from hospital_news.models import (
    NewsModel, NewsGalleryModel
)
from hospital_contact.models import CareersModel
from hospital_ipd.models import IPDModel
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from extentions.validations import name_val, file_val, email_val, phone_val, national_code_val
from extentions.customs import CustomizedForm, CustomizeModelForm


class EditInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'profile']
        widgets = {
            'email': forms.EmailInput({'placeholder': _('ایمیل خود را وارد کنید')}),
        }

    def clean_profile(self):
        data = self.cleaned_data.get('profile')
        output = file_val(file=data, file_type='image', required=False)
        return output

    def clean_email(self):
        data = self.cleaned_data.get('email')
        output = email_val(email=data, ischeck_unique=False, required=False)
        return output


class SkillForm(forms.ModelForm):
    class Meta:
        model = TitleSkillModel
        fields = '__all__'

    def clean_title_fa(self):
        data = self.cleaned_data.get('title_fa')
        output = name_val(name=data, required=True)
        return output
    def clean_title_en(self):
        data = self.cleaned_data.get('title_en')
        output = name_val(name=data, required=True)
        return output
    def clean_title_ar(self):
        data = self.cleaned_data.get('title_ar')
        output = name_val(name=data, required=True)
        return output
    def clean_title_ru(self):
        data = self.cleaned_data.get('title_ru')
        output = name_val(name=data, required=True)
        return output


class DegreeForm(forms.ModelForm):
    class Meta:
        model = DegreeModel
        fields = '__all__'

    def clean_title_fa(self):
        data = self.cleaned_data.get('title_fa')
        output = name_val(name=data, required=True)
        return output
    def clean_title_en(self):
        data = self.cleaned_data.get('title_en')
        output = name_val(name=data, required=True)
        return output
    def clean_title_ar(self):
        data = self.cleaned_data.get('title_ar')
        output = name_val(name=data, required=True)
        return output
    def clean_title_ru(self):
        data = self.cleaned_data.get('title_ru')
        output = name_val(name=data, required=True)
        return output


class UnitForm(forms.ModelForm):
    class Meta:
        model = UnitModel
        fields = '__all__'

    def clean_title_fa(self):
        data = self.cleaned_data.get('title_fa')
        output = name_val(name=data, required=False)
        return output
    def clean_title_en(self):
        data = self.cleaned_data.get('title_en')
        output = name_val(name=data, required=False)
        return output
    def clean_title_ar(self):
        data = self.cleaned_data.get('title_ar')
        output = name_val(name=data, required=False)
        return output
    def clean_title_ru(self):
        data = self.cleaned_data.get('title_ru')
        output = name_val(name=data, required=False)
        return output

    def clean_image(self):
        data = self.cleaned_data.get('image')
        output = file_val(file=data, file_type='image', required=False)
        return output

    def clean_manager_phone(self):
        data = self.cleaned_data.get('manager_phone')
        output = phone_val(phone=data, required=False)
        return output

    def clean_email(self):
        data = self.cleaned_data.get('email')
        output = email_val(email=data, ischeck_unique=False, required=False)
        return output

    def clean_icon(self):
        data = self.cleaned_data.get('icon')
        output = file_val(file=data, file_type='image', required=False)
        return output


class SubUnitForm(forms.ModelForm):
    class Meta:
        model = SubUnitModel
        exclude = ['slug']

    def clean_title_fa(self):
        title_fa = self.cleaned_data.get('title_fa') 
        category = self.cleaned_data.get('category') 
        if SubUnitModel.objects.filter(category=category, title_fa=title_fa).exists():
            raise forms.ValidationError(_('این آیتم در جدول موجود میباشد.'))
        if SubUnitModel.objects.filter(title_fa=title_fa).exists():
            raise forms.ValidationError(_('شما یک داده با این نام ثبت کرده اید.'))
        return title_fa

    def clean_title_en(self):
        title_en = self.cleaned_data.get('title_en') 
        category = self.cleaned_data.get('category') 
        if SubUnitModel.objects.filter(category=category, title_en=title_en).exists():
            raise forms.ValidationError(_('این آیتم در جدول موجود میباشد.'))
        if SubUnitModel.objects.filter(title_en=title_en).exists():
            raise forms.ValidationError(_('شما یک داده با این نام ثبت کرده اید.'))
        return title_en

    def clean_title_ar(self):
        title_ar = self.cleaned_data.get('title_ar') 
        category = self.cleaned_data.get('category') 
        if SubUnitModel.objects.filter(category=category, title_ar=title_ar).exists():
            raise forms.ValidationError(_('این آیتم در جدول موجود میباشد.'))
        if SubUnitModel.objects.filter(title_ar=title_ar).exists():
            raise forms.ValidationError(_('شما یک داده با این نام ثبت کرده اید.'))
        return title_ar

    def clean_title_ru(self):
        title_ru = self.cleaned_data.get('title_ru') 
        category = self.cleaned_data.get('category') 
        if SubUnitModel.objects.filter(category=category, title_ru=title_ru).exists():
            raise forms.ValidationError(_('این آیتم در جدول موجود میباشد.'))
        if SubUnitModel.objects.filter(title_ru=title_ru).exists():
            raise forms.ValidationError(_('شما یک داده با این نام ثبت کرده اید.'))
        return title_ru


class LimitTurnTimeForm(forms.ModelForm):

    class Meta:
        model = LimitTurnTimeModel
        fields = '__all__'

    def clean_hours(self):
        hours = self.cleaned_data.get('hours')
        if not hours:
            raise forms.ValidationError(_('عدد ساعت را وارد کنید.'))
        if hours >= 168:
            raise forms.ValidationError(_('عدد ساعت نباید بزرگتر از 168 یا یک هفته باشد.'))
        if hours <= 0:
            raise forms.ValidationError(_('عدد ساعت باید بیشتر از 1 ساعت باشد.'))
        return hours

    def clean_rules(self):
        rules = self.cleaned_data.get('rules')
        if not rules:
            raise forms.ValidationError(_('قوانین را وارد کنید.'))
        return rules


class InsuranceForm(forms.ModelForm):
    
    class Meta:
        model = InsuranceModel
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) >= 90:
            raise forms.ValidationError(_('مقدار فیلد نباید بزرگتر از 90 کاراکتر باشد.'))
        if InsuranceModel.objects.filter(title=title).exists():
            raise forms.ValidationError(_('شما قبلا یک مقدار شبیه به این داده ثبت کرده اید.'))
        return title

    def clean_img(self):
        data = self.cleaned_data.get('img')
        output = file_val(file=data, file_type='image', required=True)
        return output


class AppointmentTipForm(forms.ModelForm):

    class Meta:
        model = AppointmentTipModel
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) >= 90:
            raise forms.ValidationError(_('مقدار فیلد نباید بزرگتر از 90 کاراکتر باشد.'))
        if AppointmentTipModel.objects.filter(title=title).exists():
            raise forms.ValidationError(_('شما قبلا یک مقدار شبیه به این داده ثبت کرده اید.'))
        return title


class AppointmentTipSMSForm(forms.ModelForm):
    class Meta:
        model = AppointmentTipSMSModel
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) >= 90:
            raise forms.ValidationError(_('مقدار فیلد نباید بزرگتر از 90 کاراکتر باشد.'))
        if AppointmentTipModel.objects.filter(title=title).exists():
            raise forms.ValidationError(_('شما قبلا یک مقدار شبیه به این داده ثبت کرده اید.'))
        return title


class Time1AppointmentForm(forms.ModelForm):
    class Meta:
        model = AppointmentTimeModel
        fields = ['doctor']


class Time2AppointmentForm(forms.ModelForm):
    date_from = forms.DateField(widget=forms.DateInput())
    date_to = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = AppointmentTimeModel
        fields = ['date_from', 'date_to', 'time_from', 'time_to', 'capacity', 'tip', 'tip_sms']

    def __init__(self, *args, **kwargs):
        super(Time2AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['date_from'] = JalaliDateField(label=_('از تاریخ'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget
        )
        self.fields['date_to'] = JalaliDateField(label=_('تا تاریخ'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget
        )


    def clean_date_from(self):
        date_from = self.cleaned_data.get('date_from')
        if bool(datetime.datetime.now().date() > date_from):
            raise forms.ValidationError(_('تاریخ نباید از زمان حال کوچکتر باشد.'))
        return date_from

    def clean_date_to(self):
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')

        if bool(datetime.datetime.now().date() > date_to):
            raise forms.ValidationError(_('تاریخ نباید از زمان حال کوچکتر باشد.'))

        if date_from > date_to:
            raise forms.ValidationError(_('تاریخ مقصد نباید از تاریخ مبدا کوچکتر باشد.'))
        return date_to
    
    def clean_time_to(self):
        time_from = self.cleaned_data.get('time_from')
        time_to = self.cleaned_data.get('time_to')

        time_from_str = time_from.split(':')
        time_to_str = time_to.split(':')

        if int(time_to_str[0]) < int(time_from_str[0]):
            raise forms.ValidationError(_('ساعت مقصد نباید از ساعت مبدا کوچکتر باشد.'))
        if int(time_to_str[0]) == int(time_from_str[0]):
            if int(time_to_str[1]) <= int(time_from_str[1]):
                raise forms.ValidationError(_('ساعت مقصد نباید از ساعت مبدا کوچکتر باشد.'))
        return time_to


class AllAppointmentForm(forms.ModelForm):

    class Meta:
        model = AppointmentTimeModel
        fields = ['time_from', 'time_to', 'capacity', 'status', 'tip', 'tip_sms']

    def clean_time_to(self):
        time_from = self.cleaned_data.get('time_from')
        time_to = self.cleaned_data.get('time_to')

        time_from_str = time_from.split(':')
        time_to_str = time_to.split(':')

        if int(time_to_str[0]) < int(time_from_str[0]):
            raise forms.ValidationError(_('ساعت مقصد نباید از ساعت مبدا کوچکتر باشد.'))
        if int(time_to_str[0]) == int(time_from_str[0]):
            if int(time_to_str[1]) <= int(time_from_str[1]):
                raise forms.ValidationError(_('ساعت مقصد نباید از ساعت مبدا کوچکتر باشد.'))
        return time_to


class DoctorForm(forms.ModelForm):
    class Meta:
        model = DoctorModel
        fields = '__all__'


class DoctorEditForm(forms.ModelForm):
    class Meta:
        model = DoctorModel
        exclude = ['id', 'insurances', 'medical_code', 'user', 'unit', 'is_medicalteam', 'is_intenational', 'is_public', 'is_clinic', 'is_active']


class DoctorVacationForm(forms.ModelForm):
    class Meta:
        model = DoctorVacationModel
        fields = ['from_date', 'to_date', 'from_time', 'to_time'] 

    def __init__(self, *args, **kwargs):
        super(DoctorVacationForm, self).__init__(*args, **kwargs)
        self.fields['from_date'] = JalaliDateField(label=_('از تاریخ'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget
        )
        self.fields['to_date'] = JalaliDateField(label=_('تا تاریخ'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget
        )

    def clean_from_date(self):
        from_date = self.cleaned_data.get('from_date')
        if bool(datetime.datetime.now().date() > from_date):
            raise forms.ValidationError(_('تاریخ نباید از زمان حال کوچکتر باشد.'))
        return from_date

    def clean_to_date(self):
        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')

        if bool(datetime.datetime.now().date() > to_date):
            raise forms.ValidationError(_('تاریخ نباید از زمان حال کوچکتر باشد.'))

        if from_date > to_date:
            raise forms.ValidationError(_('تاریخ مقصد نباید از تاریخ مبدا کوچکتر باشد.'))
        return to_date

    def clean_to_time(self):
        from_time = self.cleaned_data.get('from_time')
        to_time = self.cleaned_data.get('to_time')

        from_time_str = from_time.split(':')
        to_time_str = to_time.split(':')

        if int(to_time_str[0]) < int(from_time_str[0]):
            raise forms.ValidationError(_('ساعت مقصد نباید از ساعت مبدا کوچکتر باشد.'))
        if int(to_time_str[0]) == int(from_time_str[0]):
            if int(to_time_str[1]) <= int(from_time_str[1]):
                raise forms.ValidationError(_('ساعت مقصد نباید از ساعت مبدا کوچکتر باشد.'))
        return to_time


class DoctorWorkForm(forms.ModelForm):
    class Meta:
        model = DoctorWorkTimeModel
        fields = ['day_from', 'day_to', 'time_from', 'time_to'] 


class ElectronicPrescriptionForm(forms.ModelForm):
    selected_date = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = ElectronicPrescriptionModel
        fields = ['doctor', 'unit', 'selected_date', 'selected_time'] 

    def __init__(self, *args, **kwargs):
        super(ElectronicPrescriptionForm, self).__init__(*args, **kwargs)
        self.fields['selected_date'] = JalaliDateField(label=_('تاریخ حضور'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget
        )


class ExprimentResultForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = ExprimentResultModel
        exclude = ['code']

    def __init__(self, *args, **kwargs):
        super(ExprimentResultForm, self).__init__(*args, **kwargs)
        self.fields['date'] = JalaliDateField(label=_('تاریخ'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget
        )

    def clean_title(self):
        data = self.cleaned_data.get('title')
        output = name_val(name=data, required=True)
        return output

    def clean_result(self):
        data = self.cleaned_data.get('result')
        output = name_val(name=data, required=False)
        return output

    def clean_image(self):
        data = self.cleaned_data.get('image')
        output = file_val(file=data, file_type='image', required=False)
        return output


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        exclude = ['slug', 'qr_img', 'writer']
    
    def clean_image(self):
        data = self.cleaned_data.get('image')
        output = file_val(file=data, file_type='image', required=True)
        return output

    def clean_pdf(self):
        data = self.cleaned_data.get('pdf')
        output = file_val(file=data, file_type='text', required=False)
        return output

    def clean_title_fa(self):
        data = self.cleaned_data.get('title_fa')
        output = name_val(name=data, required=True)
        return output
    def clean_title_en(self):
        data = self.cleaned_data.get('title_en')
        output = name_val(name=data, required=True)
        return output
    def clean_title_ar(self):
        data = self.cleaned_data.get('title_ar')
        output = name_val(name=data, required=True)
        return output
    def clean_title_ru(self):
        data = self.cleaned_data.get('title_ru')
        output = name_val(name=data, required=True)
        return output


class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsModel
        exclude = ['slug', 'writer']

    def clean_image(self):
        data = self.cleaned_data.get('image')
        output = file_val(file=data, file_type='image', required=True)
        return output

    def clean_title_fa(self):
        data = self.cleaned_data.get('title_fa')
        output = name_val(name=data, required=True)
        return output
    def clean_title_en(self):
        data = self.cleaned_data.get('title_en')
        output = name_val(name=data, required=True)
        return output
    def clean_title_ar(self):
        data = self.cleaned_data.get('title_ar')
        output = name_val(name=data, required=True)
        return output
    def clean_title_ru(self):
        data = self.cleaned_data.get('title_ru')
        output = name_val(name=data, required=True)
        return output


class TagForm(forms.ModelForm):
    class Meta:
        model = TagModel
        fields = '__all__'

    def clean_title_fa(self):
        title_fa = self.cleaned_data.get('title_fa')
        if TagModel.objects.filter(title_fa__iexact=title_fa).first():
            raise forms.ValidationError(_('شما قبلا یک تگ با همین نام ایجاد کرده اید.'))
        return title_fa
    def clean_title_en(self):
        title_en = self.cleaned_data.get('title_en')
        if TagModel.objects.filter(title_en__iexact=title_en).first():
            raise forms.ValidationError(_('شما قبلا یک تگ با همین نام ایجاد کرده اید.'))
        return title_en
    def clean_title_ar(self):
        title_ar = self.cleaned_data.get('title_ar')
        if TagModel.objects.filter(title_ar__iexact=title_ar).first():
            raise forms.ValidationError(_('شما قبلا یک تگ با همین نام ایجاد کرده اید.'))
        return title_ar
    def clean_title_ru(self):
        title_ru = self.cleaned_data.get('title_ru')
        if TagModel.objects.filter(title_ru__iexact=title_ru).first():
            raise forms.ValidationError(_('شما قبلا یک تگ با همین نام ایجاد کرده اید.'))
        return title_ru


class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = '__all__'

    def clean_title_fa(self):
        title_fa = self.cleaned_data.get('title_fa')
        if CategoryModel.objects.filter(title_fa__iexact=title_fa).first():
            raise forms.ValidationError(_('شما قبلا یک عنوان دسته بندی با همین نام ایجاد کرده اید.'))
        return title_fa
    def clean_title_en(self):
        title_en = self.cleaned_data.get('title_en')
        if CategoryModel.objects.filter(title_en__iexact=title_en).first():
            raise forms.ValidationError(_('شما قبلا یک عنوان دسته بندی با همین نام ایجاد کرده اید.'))
        return title_en
    def clean_title_ar(self):
        title_ar = self.cleaned_data.get('title_ar')
        if CategoryModel.objects.filter(title_ar__iexact=title_ar).first():
            raise forms.ValidationError(_('شما قبلا یک عنوان دسته بندی با همین نام ایجاد کرده اید.'))
        return title_ar
    def clean_title_ru(self):
        title_ru = self.cleaned_data.get('title_ru')
        if CategoryModel.objects.filter(title_ru__iexact=title_ru).first():
            raise forms.ValidationError(_('شما قبلا یک عنوان دسته بندی با همین نام ایجاد کرده اید.'))
        return title_ru


class BlogGalleryForm(forms.ModelForm):
    class Meta:
        model = BlogGalleryModel
        fields = '__all__'

    def clean_image(self):
        data = self.cleaned_data.get('image')
        output = file_val(file=data, file_type='image', required=False)
        return output

    def clean(self):
        image = self.cleaned_data.get('image')
        video_link = self.cleaned_data.get('video_link')

        if not image and not video_link:
            raise forms.ValidationError(_('هر دو فیلد نمیتوانند خالی باشند.'))
        if image and video_link:
            raise forms.ValidationError(_('هر دو فیلد نمیتوانند مقدار داشته باشند.'))


class NewsGalleryForm(forms.ModelForm):
    class Meta:
        model = NewsGalleryModel
        fields = '__all__'
    
    def clean_image(self):
        data = self.cleaned_data.get('image')
        output = file_val(file=data, file_type='image', required=False)
        return output

    def clean(self):
        image = self.cleaned_data.get('image')
        video_link = self.cleaned_data.get('video_link')

        if not image and not video_link:
            raise forms.ValidationError(_('هر دو فیلد نمیتوانند خالی باشند.'))
        if image and video_link:
            raise forms.ValidationError(_('هر دو فیلد نمیتوانند مقدار داشته باشند.'))


class PatientForm(CustomizeModelForm):
    class Meta:
        model = PatientModel
        fields = '__all__'

    def clean_username(self):
        data = self.cleaned_data.get('username')
        output = national_code_val(national_code=data, ischeck_unique=False, required=True)
        return output

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        output = name_val(name=data, required=True)
        return output

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        output = name_val(name=data, required=True)
        return output

    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        output = phone_val(phone=data, required=True)
        return output


class MedicalNoteForm(forms.ModelForm):
    class Meta:
        model = MedicalNoteModel
        fields = '__all__'


class SMSTextForm(forms.ModelForm):
    class Meta:
        model = SMSTextModel
        fields = '__all__'


class PampheletForm(forms.ModelForm):
    class Meta:
        model = PampheletModel
        fields = '__all__'

    def clean_image(self):
        data = self.cleaned_data.get('image')
        output = file_val(file=data, file_type='image', required=True)
        return output

    def clean_title_fa(self):
        data = self.cleaned_data.get('title_fa')
        output = name_val(name=data, required=True)
        return output
    def clean_title_en(self):
        data = self.cleaned_data.get('title_en')
        output = name_val(name=data, required=True)
        return output
    def clean_title_ar(self):
        data = self.cleaned_data.get('title_ar')
        output = name_val(name=data, required=True)
        return output
    def clean_title_ru(self):
        data = self.cleaned_data.get('title_ru')
        output = name_val(name=data, required=True)
        return output


class CareersForm(forms.ModelForm):
    class Meta:
        model = CareersModel
        exclude = ['code']

    def clean_title(self):
        data = self.cleaned_data.get('title')
        output = name_val(name=data, required=True)
        return output

    def clean_image(self):
        data = self.cleaned_data.get('image')
        output = file_val(file=data, file_type='image', required=False)
        return output


class IPDAnswerForm(forms.ModelForm):
    class Meta:
        model = IPDModel
        fields = ['answer']

    def clean_answer(self):
        answer = self.cleaned_data.get('answer')
        if not answer:
            raise forms.ValidationError(_('محتوای فیلد را وارد کنید.'))
        return answer
    

