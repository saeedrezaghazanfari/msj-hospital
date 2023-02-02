from django import forms
from django.utils.translation import gettext_lazy as _
from .models import HireFormModel, CriticismSuggestionModel, ContactUsModel
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from extentions.validations import national_code_val, name_val, phone_val, email_val, file_val


class HireForm(forms.ModelForm):
    birthday_date = forms.DateField(widget=forms.DateInput())
    end_date = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = HireFormModel
        exclude = ['career', 'created', 'is_checked']

    def __init__(self, *args, **kwargs):
        super(HireForm, self).__init__(*args, **kwargs)
        self.fields['birthday_date'] = JalaliDateField(label=_('تاریخ تولد'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget
        )
        self.fields['end_date'] = JalaliDateField(label=_('تاریخ پایان طرح'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget
        )

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        output = name_val(name=data, required=True)
        return output

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        output = name_val(name=data, required=True)
        return output

    def clean_father(self):
        data = self.cleaned_data.get('father')
        output = name_val(name=data, required=True)
        return output

    def clean_national_code(self):
        data = self.cleaned_data.get('national_code')
        output = national_code_val(national_code=data, ischeck_unique=False, required=True)
        return output

    def clean_birthday_place(self):
        data = self.cleaned_data.get('birthday_place')
        output = name_val(name=data, required=True)
        return output

    def clean_direct(self):
        data = self.cleaned_data.get('direct')
        output = name_val(name=data, required=False)
        return output

    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        output = phone_val(phone=data, required=True)
        return output

    def clean_email(self):
        data = self.cleaned_data.get('email')
        output = email_val(email=data, ischeck_unique=False, required=False)
        return output

    def clean_resume(self):
        data = self.cleaned_data.get('resume')
        output = file_val(file=data, file_type='text', required=True)
        return output


class CriticismSuggestionForm(forms.ModelForm):
    class Meta:
        model = CriticismSuggestionModel
        exclude = ['code', 'is_read', 'created']

    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        output = name_val(name=data, required=True)
        return output

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        output = name_val(name=data, required=True)
        return output
    
    def clean_national_code(self):
        data = self.cleaned_data.get('national_code')
        output = national_code_val(national_code=data, ischeck_unique=False, required=True)
        return output

    def clean_email(self):
        data = self.cleaned_data.get('email')
        output = email_val(email=data, ischeck_unique=False, required=False)
        return output
    
    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        output = phone_val(phone=data, required=True)
        return output
    
    def clean_manager(self):
        data = self.cleaned_data.get('manager')
        output = name_val(name=data, required=True)
        return output


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUsModel
        exclude = ['is_read', 'created']

    def clean_name(self):
        data = self.cleaned_data.get('name')
        output = name_val(name=data, required=True)
        return output

    def clean_email(self):
        data = self.cleaned_data.get('email')
        output = email_val(email=data, ischeck_unique=False, required=True)
        return output

    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        output = phone_val(phone=data, required=True)
        return output

    def clean_title(self):
        data = self.cleaned_data.get('title')
        output = name_val(name=data, required=True)
        return output

