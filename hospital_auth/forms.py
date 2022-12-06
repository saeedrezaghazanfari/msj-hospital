import re
from django import forms
from .models import User
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from extentions.utils import is_phone, is_national_code


class SignUpForm(forms.ModelForm):
    GENDER_USER = (('male', _('مرد')), ('female', _('زن')))
    gender = forms.ChoiceField(
        choices=GENDER_USER, 
        widget=forms.RadioSelect(attrs={'name': 'gender_radio', 'checked': 'checked'})
    )
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'gender']
        widgets = {
            'username': forms.TextInput({'placeholder': _('کدملی خود را وارد کنید')}),
            'first_name': forms.TextInput({'placeholder': _('نام خود را وارد کنید')}),
            'last_name': forms.TextInput({'placeholder': _('نام خانوادگی خود را وارد کنید')}),
            'phone': forms.NumberInput({'placeholder': _('شماره تلفن خود را وارد کنید')}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(_('کدملی خود را وارد کنید'))
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('کدملی شما یک بار در سیستم ثبت شده است'))
        if not username.isdigit():
            raise forms.ValidationError(_('کدملی باید شامل اعداد باشد'))
        if not is_national_code(username):
            raise forms.ValidationError(_('الگوی کدملی شما صحیح نیست'))
        return username

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
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or phone == 0:
            raise forms.ValidationError(_('شماره تلفن خود را وارد کنید'))
        if User.objects.filter(phone=phone).first():
            raise forms.ValidationError(_('این شماره تلفن در سیستم ثبت شده است'))
        if not is_phone(phone):
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست'))
        return phone


class SignInForm(forms.Form):
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': _('شماره تلفن خود را وارد کنید') }))
    captcha = CaptchaField()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError(_('شماره تلفن همراه خود را وارد کنید'))        
        if not User.objects.filter(phone=phone).first():
            raise forms.ValidationError(_('این شماره تلفن در سیستم موجود نیست'))
        if not is_phone(phone):
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست'))
        return phone


class EnterCodePWForm(forms.Form):
    code = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': _('مانند: 12345')}))

    def clean_code(self):
        code = self.cleaned_data.get('code')
        is_code = bool(re.compile(r'[0-9]{5}').match(str(code)))
        
        if not code:
            raise forms.ValidationError(_('کد پیامک شده را وارد کنید'))
        if not is_code:
            raise forms.ValidationError(_('فرمت کد قابل قبول نیست'))
        return code


