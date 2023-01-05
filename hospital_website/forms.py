import re
from django.utils import timezone
from django import forms
from hospital_auth.models import User, PatientModel
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from hospital_setting.models import PriceAppointmentModel
from hospital_units.models import AppointmentTimeModel, PatientTurnModel, ElectronicPrescriptionModel
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from .models import LoginCodePatientModel
from captcha.fields import CaptchaField
from extentions.utils import is_phone, is_national_code

class PhoneForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput())
    captcha = CaptchaField()
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or phone == 0 or len(phone) == 0:
            raise forms.ValidationError(_('تلفن همراه خود را وارد کنید.'))
        if not is_phone(phone):
            raise forms.ValidationError(_('الگوی تلفن همراه شما صحیح نیست.'))
        return phone


class EnterCodePhoneForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput())

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code or int(code) == 0 or len(code) == 0:
            raise forms.ValidationError(_('کد پیامک شده را وارد کنید.'))
        if not re.compile(r'(^\d{5}$)').match(code):
            raise forms.ValidationError(_('الگوی کد پیامک شده شما صحیح نیست.'))
        if not LoginCodePatientModel.objects.filter(code=int(code), expire_date__gt=timezone.now(), is_use=False).exists():
            forms.ValidationError(_('کد شما منقضی شده و یا اینکه اعتبار ندارد.'))
        return code


class PriceAppointmentForm(forms.ModelForm):
    class Meta:
        model = PriceAppointmentModel
        fields = ['insurance', 'degree', 'price']

    def clean_price(self):
        value = self.cleaned_data.get('price')
        if value == 0:
            raise forms.ValidationError(_('مقدار فیلد را وارد کنید.'))
        if value < 0:
            raise forms.ValidationError(_('مقدار این فیلد نمیتواند منفی باشد.'))
        return value


class TimeAppointmentForm(forms.ModelForm):
    date_from = forms.DateField(widget=forms.DateInput())
    date_to = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = AppointmentTimeModel
        fields = ['unit', 'doctor', 'date_from', 'date_to', 'time_from', 'time_to', 'insurances', 'capacity', 'tip']

    def __init__(self, *args, **kwargs):
        super(TimeAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['date_from'] = JalaliDateField(label=_('از تاریخ'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget
        )
        self.fields['date_to'] = JalaliDateField(label=_('تا تاریخ'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget
        )
        # self.fields['date'] = SplitJalaliDateTimeField(label=_('تاریخ روز'), 
        #     widget=AdminSplitJalaliDateTime # required, for decompress DatetimeField to JalaliDateField and JalaliTimeField
        # )

    def clean_date_to(self):
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
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


class PatientForm(forms.ModelForm):
    GENDER_USER = (('male', _('مرد')), ('female', _('زن')))

    username = forms.CharField(widget=forms.TextInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    gender = forms.CharField(widget=forms.Select(choices=GENDER_USER))
    age = forms.IntegerField(widget=forms.NumberInput())

    class Meta:
        model = PatientTurnModel
        fields = [
            'prescription_code', 'experiment_code', 'username', 
            'first_name', 'last_name', 'gender', 'age'
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(_('کدملی خود را وارد کنید'))
        if not username.isdigit():
            raise forms.ValidationError(_('کدملی باید شامل اعداد باشد'))
        if not is_national_code(username):
            raise forms.ValidationError(_('الگوی کدملی شما صحیح نیست'))
        return username

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not age:
            raise forms.ValidationError(_('سن خود را وارد کنید'))
        if age < 0:
            raise forms.ValidationError(_('سن نباید منفی باشد.'))
        if age > 120:
            raise forms.ValidationError(_('عدد سن معتبر نیست.'))
        return age

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError(_('نام خود را وارد کنید'))
        if len(first_name) <= 1:
            raise forms.ValidationError(_('نام باید بیشتر از 1 کاراکتر باشد'))
        if len(first_name) >= 20:
            raise forms.ValidationError(_('نام باید کمتر از 20 کاراکتر باشد'))
        for i in first_name:
            if i.isdigit():
                raise forms.ValidationError(_('نام باید شامل کاراکترهای غیر از اعداد باشد'))
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError(_('نام‌خانوادگی خود را وارد کنید'))
        if len(last_name) <= 1:
            raise forms.ValidationError(_('نام‌خانوادگی باید بیشتر از 1 کاراکتر باشد'))
        if len(last_name) >= 25:
            raise forms.ValidationError(_('نام‌خانوادگی باید کمتر از 25 کاراکتر باشد'))
        for i in last_name:
            if i.isdigit():
                raise forms.ValidationError(_('نام‌خانوادگی باید شامل کاراکترهای غیر از اعداد باشد'))
        return last_name


class ElectronicPrescriptionForm(forms.ModelForm):
    GENDER_USER = (('male', _('مرد')), ('female', _('زن')))

    username = forms.CharField(widget=forms.TextInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    gender = forms.CharField(widget=forms.Select(choices=GENDER_USER))
    age = forms.IntegerField(widget=forms.NumberInput())

    class Meta:
        model = ElectronicPrescriptionModel
        fields = [
            'experiment_code', 'username', 
            'first_name', 'last_name', 'gender', 'age'
        ]

    def clean_experiment_code(self):
        experiment_code = self.cleaned_data.get('experiment_code')
        if not experiment_code:
            raise forms.ValidationError(_('کدرهگیری خود را وارد کنید'))
        if not experiment_code.isdigit():
            raise forms.ValidationError(_('کدرهگیری باید شامل اعداد باشد'))
        if not is_national_code(experiment_code):
            raise forms.ValidationError(_('الگوی کدرهگیری شما صحیح نیست'))
        return experiment_code

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(_('کدملی خود را وارد کنید'))
        if not username.isdigit():
            raise forms.ValidationError(_('کدملی باید شامل اعداد باشد'))
        if not is_national_code(username):
            raise forms.ValidationError(_('الگوی کدملی شما صحیح نیست'))
        return username

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not age:
            raise forms.ValidationError(_('سن خود را وارد کنید'))
        if age < 0:
            raise forms.ValidationError(_('سن نباید منفی باشد.'))
        if age > 120:
            raise forms.ValidationError(_('عدد سن معتبر نیست.'))
        return age

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError(_('نام خود را وارد کنید'))
        if len(first_name) <= 1:
            raise forms.ValidationError(_('نام باید بیشتر از 1 کاراکتر باشد'))
        if len(first_name) >= 20:
            raise forms.ValidationError(_('نام باید کمتر از 20 کاراکتر باشد'))
        for i in first_name:
            if i.isdigit():
                raise forms.ValidationError(_('نام باید شامل کاراکترهای غیر از اعداد باشد'))
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError(_('نام‌خانوادگی خود را وارد کنید'))
        if len(last_name) <= 1:
            raise forms.ValidationError(_('نام‌خانوادگی باید بیشتر از 1 کاراکتر باشد'))
        if len(last_name) >= 25:
            raise forms.ValidationError(_('نام‌خانوادگی باید کمتر از 25 کاراکتر باشد'))
        for i in last_name:
            if i.isdigit():
                raise forms.ValidationError(_('نام‌خانوادگی باید شامل کاراکترهای غیر از اعداد باشد'))
        return last_name

class CheckRulesForm(forms.Form):
    check_rules = forms.BooleanField(required=False, widget=forms.widgets.CheckboxInput())

    def clean_check_rules(self):
        check_rules = self.cleaned_data.get('check_rules')
        if not check_rules:
            raise forms.ValidationError(_('تنها در صورتی میتوانید نوبت اینترنتی رزرو کنید که با قوانین و مقررات موافق باشید.'))
        return check_rules
