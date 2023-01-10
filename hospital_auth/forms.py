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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(_('کدملی خود را وارد کنید'))
        if not username.isdigit():
            raise forms.ValidationError(_('کدملی باید شامل اعداد باشد'))
        if not is_national_code(username):
            raise forms.ValidationError(_('الگوی کدملی شما صحیح نیست'))
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('کدملی شما یک بار در سیستم ثبت شده است'))
        return username

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
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone or phone == 0:
            raise forms.ValidationError(_('شماره تلفن خود را وارد کنید'))
        if not is_phone(phone):
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست'))
        if User.objects.filter(phone=phone).first():
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
        if not User.objects.filter(phone=phone).first():
            raise forms.ValidationError(_('این شماره تلفن در سیستم موجود نیست'))
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


