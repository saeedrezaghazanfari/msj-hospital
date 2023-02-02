from django import forms
from django.utils.translation import gettext_lazy as _
from hospital_auth.models import User
from .utils import (
    is_national_code, is_phone, is_email, is_text, is_video, is_image, is_audio
)


def national_code_val(national_code, ischeck_unique, required):
    if (required) or (not required and national_code):
        if not national_code:
            raise forms.ValidationError(_('کدملی خود را وارد کنید.'))
        if not is_national_code(national_code):
            raise forms.ValidationError(_('الگوی کدملی شما صحیح نیست.'))
        if ischeck_unique == True:
            if User.objects.filter(username=national_code).exists():
                raise forms.ValidationError(_('کدملی شما یک بار در سیستم ثبت شده است.'))
        return national_code


def name_val(name, required):
    if (required) or (not required and name):
        if not name:
            raise forms.ValidationError(_('محتوای فیلد را وارد کنید.'))
        if len(name) <= 1:
            raise forms.ValidationError(_('این فیلد باید بیشتر از 1 کاراکتر باشد.'))
        if len(name) >= 255:
            raise forms.ValidationError(_('این فیلد باید کمتر از 255 کاراکتر باشد.'))
        for i in name:
            if i.isdigit():
                raise forms.ValidationError(_('این فیلد باید شامل کاراکترهای غیر از اعداد باشد.'))
        return name


def phone_val(phone, required):
    if (required) or (not required and phone):
        if not phone or phone == 0:
            raise forms.ValidationError(_('شماره تلفن خود را وارد کنید.'))
        if not is_phone(phone):
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست.'))
        return phone


def email_val(email, ischeck_unique, required):
    if (required) or (not required and email):
        if not is_email(email):
            raise forms.ValidationError(_('الگوی ایمیل شما صحیح نیست.'))
        if ischeck_unique == True:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(_('قبلا این آدرس ایمیل در سیستم ثبت شده است.'))
        return email


def file_val(file, file_type, required):
    if (required) or (not required and file):
        if file_type == 'text':
            if not is_text(file):
                raise forms.ValidationError(_('فرمت فایل شما باید pdf باشد.'))

        elif file_type == 'video':
            if not is_video(file):
                raise forms.ValidationError(_('فرمت فایل شما باید یکی از فرمت های mp4, webm, mkv باشد.'))

        elif file_type == 'image':
            if not is_image(file):
                raise forms.ValidationError(_('فرمت فایل شما باید یکی از فرمت های jpg, jpeg, png باشد.'))

        elif file_type == 'audio':
            if not is_audio(file):
                raise forms.ValidationError(_('فرمت فایل شما باید mp3 باشد.'))
        return file
