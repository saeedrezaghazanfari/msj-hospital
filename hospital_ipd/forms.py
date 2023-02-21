import re
from django.utils import timezone
from django import forms
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from extentions.validations import (
    name_val, phone_val, email_val, file_val, age_val
)
from extentions.utils import is_passport, is_national_code
from .models import IPDModel, IPDCodeModel
from extentions.customs import CustomizedForm, CustomizedModelForm


class PhoneForm(CustomizedForm):
    phone = forms.CharField(widget=forms.TextInput())
    captcha = CaptchaField()
    
    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        output = phone_val(phone=data, required=True)
        return output


class LoginForm(CustomizedForm):
    phone = forms.CharField(widget=forms.TextInput())
    code = forms.CharField(widget=forms.TextInput())
    captcha = CaptchaField()
    
    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        output = phone_val(phone=data, required=True)
        return output
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code or int(code) == 0 or len(code) == 0:
            raise forms.ValidationError(_('کد پیامک شده را وارد کنید.'))
        if not re.compile(r'(^\d{11}$)').match(code):
            raise forms.ValidationError(_('الگوی کد پیامک شده شما صحیح نیست.'))
        if not IPDCodeModel.objects.filter(code=int(code), expire_date__gt=timezone.now(), is_use=False).exists():
            forms.ValidationError(_('کد شما منقضی شده و یا اینکه اعتبار ندارد.'))
        return code


class EnterCodePhoneForm(CustomizedForm):
    code = forms.CharField(widget=forms.TextInput())

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code or int(code) == 0 or len(code) == 0:
            raise forms.ValidationError(_('کد پیامک شده را وارد کنید.'))
        if not re.compile(r'(^\d{5}$)').match(code):
            raise forms.ValidationError(_('الگوی کد پیامک شده شما صحیح نیست.'))
        if not IPDCodeModel.objects.filter(code=int(code), expire_date__gt=timezone.now(), is_use=False).exists():
            forms.ValidationError(_('کد شما منقضی شده و یا اینکه اعتبار ندارد.'))
        return code


class IPDForm(CustomizedModelForm):

    class Meta:
        model = IPDModel
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'age', 'description', 'document']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise forms.ValidationError(_('شماره پاسپورت یا کد ملی خود را وارد کنید.'))
        if not is_passport(username) and not is_national_code(username):
            raise forms.ValidationError(_('الگوی کدملی یا شماره پاسپورت شما صحیح نیست.'))
        return username

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        output = name_val(name=data, required=True)
        return output

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        output = name_val(name=data, required=True)
        return output
    
    def clean_age(self):
        data = self.cleaned_data.get('age')
        output = age_val(age=data, required=True)
        return output

    def clean_email(self):
        data = self.cleaned_data.get('email')
        output = email_val(email=data, ischeck_unique=False, required=False)
        return output

    def clean_document(self):
        data = self.cleaned_data.get('document')
        output = file_val(file=data, file_type='text-image', required=False)
        return output


# class IPDForm(CustomizedModelForm):

#     class Meta:
#         model = IPDModel
#         fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'gender', 'age', 'description', 'document']