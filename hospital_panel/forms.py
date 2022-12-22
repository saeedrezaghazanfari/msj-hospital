import re
from django import forms
from hospital_auth.models import User
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from hospital_setting.models import PriceAppointmentModel
from hospital_units.models import AppointmentTimeModel
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from extentions.utils import is_fixed_phone, is_email


# class EditInfoForm(forms.Form):

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'fixed_phone', 'is_send_sms', 'email']
#         widgets = {
#             'first_name': forms.TextInput({'placeholder': _('نام خود را وارد کنید')}),
#             'last_name': forms.TextInput({'placeholder': _('نام خانوادگی خود را وارد کنید')}),
#             'fixed_phone': forms.TextInput({'placeholder': _('تلفن ثابت خود را وارد کنید')}),
#             'is_send_sms': forms.CheckboxInput({'placeholder': _('آیا مایل به دریافت پیامک های پزشکی هستید؟')}),
#             'email': forms.EmailInput({'placeholder': _('ایمیل خود را وارد کنید')}),
#         }

#     def clean_first_name(self):
#         first_name = self.cleaned_data.get('first_name')
#         if not first_name:
#             raise forms.ValidationError(_('نام خود را وارد کنید'))
#         if len(first_name) <= 1:
#             raise forms.ValidationError(_('نام باید بیشتر از 1 کاراکتر باشد'))
#         if len(first_name) >= 20:
#             raise forms.ValidationError(_('نام باید کمتر از 20 کاراکتر باشد'))
#         for i in first_name:
#             if i.isdigit():
#                 raise forms.ValidationError(_('نام باید شامل کاراکترهای غیر از اعداد باشد'))
#         return first_name
    
#     def clean_last_name(self):
#         last_name = self.cleaned_data.get('last_name')
#         if not last_name:
#             raise forms.ValidationError(_('نام‌خانوادگی خود را وارد کنید'))
#         if len(last_name) <= 1:
#             raise forms.ValidationError(_('نام‌خانوادگی باید بیشتر از 1 کاراکتر باشد'))
#         if len(last_name) >= 25:
#             raise forms.ValidationError(_('نام‌خانوادگی باید کمتر از 25 کاراکتر باشد'))
#         for i in last_name:
#             if i.isdigit():
#                 raise forms.ValidationError(_('نام‌خانوادگی باید شامل کاراکترهای غیر از اعداد باشد'))
#         return last_name

#     def clean_fixed_phone(self):
#         fixed_phone = self.cleaned_data.get('fixed_phone')
#         if not fixed_phone or fixed_phone == 0:
#             raise forms.ValidationError(_('تلفن ثابت خود را وارد کنید'))
#         if not is_fixed_phone(fixed_phone):
#             raise forms.ValidationError(_('الگوی تلفن ثابت شما صحیح نیست'))
#         return fixed_phone

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if not email or len(email) == 0:
#             raise forms.ValidationError(_('ایمیل خود را وارد کنید'))
#         if not is_email(email):
#             raise forms.ValidationError(_('الگوی ایمیل شما صحیح نیست'))
#         return email


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
        fields = ['unit', 'doctor', 'date_from', 'date_to', 'time_from', 'time_to', 'price', 'capacity', 'reserved', 'tip']

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

        if time_to_str[0] < time_from_str[0]:
            raise forms.ValidationError(_('ساعت مقصد نباید از ساعت مبدا کوچکتر باشد.'))
        if time_to_str[0] == time_from_str[0]:
            if time_to_str[1] <= time_from_str[1]:
                raise forms.ValidationError(_('ساعت مقصد نباید از ساعت مبدا کوچکتر باشد.'))
        return time_to