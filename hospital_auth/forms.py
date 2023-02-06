import re
from django import forms
from .models import User
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from extentions.validations import (
    national_code_val, name_val
)
from extentions.utils import is_phone


class SignUpForm(forms.ModelForm):
    GENDER_USER = (('male', _('مرد')), ('female', _('زن')))
    gender = forms.ChoiceField(
        choices=GENDER_USER, 
        widget=forms.RadioSelect(attrs={'name': 'gender_radio', 'checked': 'checked'})
    )
    firstname = forms.CharField(widget=forms.TextInput())
    lastname = forms.CharField(widget=forms.TextInput())
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'firstname', 'lastname', 'phone', 'gender']
        widgets = {
            'username': forms.TextInput({'placeholder': _('کدملی خود را وارد کنید')}),
            'firstname': forms.TextInput({'placeholder': _('نام خود را وارد کنید')}),
            'lastname': forms.TextInput({'placeholder': _('نام خانوادگی خود را وارد کنید')}),
            'phone': forms.NumberInput({'placeholder': _('شماره تلفن خود را وارد کنید')}),
        }

    def clean_national_code(self):
        data = self.cleaned_data.get('national_code')
        output = national_code_val(national_code=data, ischeck_unique=True, required=True)
        return output

    def clean_firstname(self):
        data = self.cleaned_data.get('firstname')
        output = name_val(name=data, required=True)
        return output
    
    def clean_lastname(self):
        data = self.cleaned_data.get('lastname')
        output = name_val(name=data, required=True)
        return output
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or phone == 0:
            raise forms.ValidationError(_('شماره تلفن خود را وارد کنید'))
        if not is_phone(phone):
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست'))
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('این شماره تلفن در سیستم ثبت شده است'))
        return phone


class SignInForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('شماره تلفن خود را وارد کنید') }))
    captcha = CaptchaField()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError(_('شماره تلفن همراه خود را وارد کنید')) 
        if not is_phone(phone):
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست'))       
        if not User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('این شماره تلفن در سیستم موجود نیست'))
        return phone


class EnterCodePWForm(forms.Form):
    code = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': _('مانند: 12345')}))

    def clean_code(self):
        code = self.cleaned_data.get('code')
        is_code = bool(re.compile(r'(^[0-9]{5}$)').match(str(code)))
        
        if not code:
            raise forms.ValidationError(_('کد پیامک شده را وارد کنید'))
        if not is_code:
            raise forms.ValidationError(_('فرمت کد قابل قبول نیست'))
        return code

