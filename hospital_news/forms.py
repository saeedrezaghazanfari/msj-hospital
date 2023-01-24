from django import forms
from django.utils.translation import gettext_lazy as _
from .models import NewsCommentModel
from extentions.utils import is_phone


class NewsCommentForm(forms.ModelForm):
    comment_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = NewsCommentModel
        fields = ['message', 'first_name', 'last_name', 'phone', 'comment_id']

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
        if not is_phone(phone):
            raise forms.ValidationError(_('الگوی شماره تلفن شما صحیح نیست'))
        return phone


class NewsReplyForm(forms.ModelForm):
    comment_id = forms.CharField(widget=forms.HiddenInput())
    news_slug = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = NewsCommentModel
        fields = ['message']


class NewsCommentEditForm(forms.ModelForm):
    comment_id = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = NewsCommentModel
        fields = ['message']