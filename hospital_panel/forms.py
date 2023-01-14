from django import forms
from hospital_auth.models import User, PatientModel
from django.utils.translation import gettext_lazy as _
from hospital_setting.models import InsuranceModel
from hospital_doctor.models import (
    DoctorModel, TitleSkillModel, DegreeModel, DoctorVacationModel, DoctorWorkTimeModel
)
from hospital_units.models import (
    UnitModel, AppointmentTimeModel, LimitTurnTimeModel, AppointmentTipModel, 
    AppointmentTipSMSModel, SubUnitModel, ElectronicPrescriptionModel, ExprimentResultModel
)
from hospital_blog.models import BlogModel
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from extentions.utils import is_email, is_image


class EditInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'profile']
        widgets = {
            'email': forms.EmailInput({'placeholder': _('ایمیل خود را وارد کنید')}),
        }

    def clean_profile(self):
        profile = self.cleaned_data.get('profile')
        if profile and not is_image(profile):
            raise forms.ValidationError(_('پسوند فایل مجاز نیست.'))
        return profile

    def clean_firstname(self):
        firstname = self.cleaned_data.get('firstname')
        if not firstname:
            raise forms.ValidationError(_('نام خود را وارد کنید'))
        if len(firstname) <= 1:
            raise forms.ValidationError(_('نام باید بیشتر از 1 کاراکتر باشد'))
        if len(firstname) >= 20:
            raise forms.ValidationError(_('نام باید کمتر از 20 کاراکتر باشد'))
        for i in firstname:
            if i.isdigit():
                raise forms.ValidationError(_('نام باید شامل کاراکترهای غیر از اعداد باشد'))
        return firstname
    
    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if not lastname:
            raise forms.ValidationError(_('نام‌خانوادگی خود را وارد کنید'))
        if len(lastname) <= 1:
            raise forms.ValidationError(_('نام‌خانوادگی باید بیشتر از 1 کاراکتر باشد'))
        if len(lastname) >= 25:
            raise forms.ValidationError(_('نام‌خانوادگی باید کمتر از 25 کاراکتر باشد'))
        for i in lastname:
            if i.isdigit():
                raise forms.ValidationError(_('نام‌خانوادگی باید شامل کاراکترهای غیر از اعداد باشد'))
        return lastname

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not is_email(email):
            raise forms.ValidationError(_('الگوی ایمیل شما صحیح نیست'))
        return email


class SkillForm(forms.ModelForm):
    class Meta:
        model = TitleSkillModel
        fields = '__all__'


class DegreeForm(forms.ModelForm):
    class Meta:
        model = DegreeModel
        fields = '__all__'


class UnitForm(forms.ModelForm):
    class Meta:
        model = UnitModel
        fields = '__all__'


class SubUnitForm(forms.ModelForm):
    class Meta:
        model = SubUnitModel
        exclude = ['slug']

    def clean_title(self):
        title = self.cleaned_data.get('title') 
        category = self.cleaned_data.get('category') 
        if SubUnitModel.objects.filter(category=category, title=title).exists():
            raise forms.ValidationError(_('این آیتم در جدول موجود میباشد.'))
        if SubUnitModel.objects.filter(title=title).exists():
            raise forms.ValidationError(_('شما یک داده با این نام ثبت کرده اید.'))
        return title


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
        if hours == 0:
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
        img = self.cleaned_data.get('img')
        if not is_image(img):
            raise forms.ValidationError(_('پسوند فایل مجاز نیست.'))
        return img


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

    def clean_date_to(self):
        from django.utils import timezone
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
        if date_from > date_to:
            raise forms.ValidationError(_('تاریخ مقصد نباید از تاریخ مبدا کوچکتر باشد.'))
        # if date_from < timezone.now().date:    #TODO
        #     raise forms.ValidationError(_('تاریخ نباید از زمان حال کوچکتر باشد.'))
        # if date_to < timezone.now().date:
        #     raise forms.ValidationError(_('تاریخ نباید از زمان حال کوچکتر باشد.'))
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

    def clean_to_date(self):
        from django.utils import timezone
        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')
        if from_date > to_date:
            raise forms.ValidationError(_('تاریخ مقصد نباید از تاریخ مبدا کوچکتر باشد.'))
        # if from_date < timezone.now().date:    #TODO
        #     raise forms.ValidationError(_('تاریخ نباید از زمان حال کوچکتر باشد.'))
        # if to_date < timezone.now().date:
        #     raise forms.ValidationError(_('تاریخ نباید از زمان حال کوچکتر باشد.'))
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


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        exclude = ['slug', 'writer']


class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientModel
        fields = '__all__'
