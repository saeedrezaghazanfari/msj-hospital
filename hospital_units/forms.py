import re
from django.utils import timezone
from django import forms
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from hospital_setting.models import PriceAppointmentModel
from .models import (
    AppointmentTimeModel, PatientTurnModel, ElectronicPrescriptionModel, 
    ExprimentResultModel, LoginCodePatientModel,
)
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from captcha.fields import CaptchaField
from hospital_extentions.validations import name_val, national_code_val, phone_val
from hospital_extentions.utils import is_phone, is_national_code
from hospital_extentions.customs import CustomizedForm, CustomizedModelForm


class PhoneForm(CustomizedForm):
    phone = forms.CharField(widget=forms.TextInput(), label=_('شماره تلفن'))
    captcha = CaptchaField(label=_('کد کپچا'))
    
    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        output = phone_val(phone=data, required=True)
        return output


class EnterCodePhoneForm(CustomizedForm):
    code = forms.CharField(widget=forms.TextInput(), label=_('کد پیامک شده'))

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code or int(code) == 0 or len(code) == 0:
            raise forms.ValidationError(_('کد پیامک شده را وارد کنید.'))
        if not re.compile(r'(^\d{5}$)').match(code):
            raise forms.ValidationError(_('الگوی کد پیامک شده شما صحیح نیست.'))
        if not LoginCodePatientModel.objects.filter(code=int(code), expire_date__gt=timezone.now(), is_use=False).exists():
            forms.ValidationError(_('کد شما منقضی شده و یا اینکه اعتبار ندارد.'))
        return code


class PriceAppointmentForm(CustomizedModelForm):
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


class TimeAppointmentForm(CustomizedModelForm):
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


class PatientForm(CustomizedModelForm):
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
        data = self.cleaned_data.get('username')
        output = national_code_val(national_code=data, ischeck_unique=False, required=True)
        return output

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
        data = self.cleaned_data.get('first_name')
        output = name_val(name=data, required=True)
        return output
    
    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        output = name_val(name=data, required=True)
        return output


class ElectronicPrescriptionForm(CustomizedModelForm):
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
            raise forms.ValidationError(_('کدرهگیری خود را وارد کنید.'))
        if not is_national_code(experiment_code):
            raise forms.ValidationError(_('الگوی کدرهگیری شما صحیح نیست.'))
        return experiment_code

    def clean_username(self):
        data = self.cleaned_data.get('username')
        output = national_code_val(national_code=data, ischeck_unique=False, required=True)
        return output

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
        data = self.cleaned_data.get('first_name')
        output = name_val(name=data, required=True)
        return output
    
    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        output = name_val(name=data, required=True)
        return output

class CheckRulesForm(CustomizedForm):
    check_rules = forms.BooleanField(required=False, widget=forms.widgets.CheckboxInput())

    def clean_check_rules(self):
        check_rules = self.cleaned_data.get('check_rules')
        if not check_rules:
            raise forms.ValidationError(_('تنها در صورتی میتوانید نوبت اینترنتی رزرو کنید که با قوانین و مقررات موافق باشید.'))
        return check_rules


class FollowUpTurnForm(CustomizedForm):
    phone = forms.CharField(widget=forms.TextInput(), label=_('شماره تلفن'))
    code = forms.CharField(widget=forms.TextInput(), label=_('کد پیامک شده'))
    captcha = CaptchaField(label=_('کد کپچا'))
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or phone == 0:
            raise forms.ValidationError(_('شماره تلفن خود را وارد کنید.'))
        if not is_phone(phone):
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست.'))
        if not PatientTurnModel.objects.filter(patient__phone=phone).exists():
            raise forms.ValidationError(_('شماره ی همراه شما در لیست وجود ندارد.'))
        return phone

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code:
            raise forms.ValidationError(_('کدپیگیری خود را وارد کنید.'))
        if not code.isdigit():
            raise forms.ValidationError(_('کدپیگیری باید شامل اعداد باشد.'))
        if not PatientTurnModel.objects.filter(code=code).exists():
            raise forms.ValidationError(_('کدپیگیری شما در لیست وجود ندارد.'))
        return code


class FollowUpResultForm(CustomizedForm):
    phone = forms.CharField(widget=forms.TextInput(), label=_('شماره تلفن'))
    code = forms.CharField(widget=forms.TextInput(), label=_('کد پیامک شده'))
    captcha = CaptchaField(label=_('کد کپچا'))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or phone == 0:
            raise forms.ValidationError(_('شماره تلفن خود را وارد کنید.'))
        if not is_phone(phone):
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست.'))
        if not ExprimentResultModel.objects.filter(patient__phone=phone).exists():
            raise forms.ValidationError(_('شماره ی همراه شما در لیست وجود ندارد.'))
        return phone

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code:
            raise forms.ValidationError(_('کدپیگیری خود را وارد کنید.'))
        if not code.isdigit():
            raise forms.ValidationError(_('کدپیگیری باید شامل اعداد باشد.'))
        if not ExprimentResultModel.objects.filter(code=code).exists():
            raise forms.ValidationError(_('کدپیگیری شما در لیست وجود ندارد.'))
        return code
