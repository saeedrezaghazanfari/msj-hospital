import re
from django.utils import timezone
from django import forms
from hospital_auth.models import User
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from hospital_setting.models import PriceAppointmentModel
from hospital_units.models import AppointmentTimeModel
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from .models import LoginCodePatientModel
from extentions.utils import is_phone


class PhoneForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput())

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
        if not LoginCodePatientModel.objects.filter(code=int(code), expire_date__gt=timezone.now(), usage='appointment', is_use=False).exists():
            forms.ValidationError(_('کد شما منقضی شده و یا اینکه اعتبار ندارد.'))
        return code


class PriceAppointmentForm(forms.ModelForm):
    class Meta:
        model = PriceAppointmentModel
        fields = ['title', 'insurance', 'degree', 'price_free', 'price_insurance', 'year']

    def clean_price_free(self):
        value = self.cleaned_data.get('price_free')
        if value == 0:
            raise forms.ValidationError(_('مقدار فیلد را وارد کنید.'))
        if value < 0:
            raise forms.ValidationError(_('مقدار این فیلد نمیتواند منفی باشد.'))
        return value
    
    def clean_price_insurance(self):
        value = self.cleaned_data.get('price_insurance')
        if value == 0:
            raise forms.ValidationError(_('مقدار فیلد را وارد کنید.'))
        if value < 0:
            raise forms.ValidationError(_('مقدار این فیلد نمیتواند منفی باشد.'))
        return value
        
    def clean_year(self):
        value = self.cleaned_data.get('year')
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
        fields = ['unit', 'doctor', 'date_from', 'date_to', 'time_from', 'time_to', 'price', 'capacity', 'tip']

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