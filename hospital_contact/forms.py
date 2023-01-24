from django import forms
from django.utils.translation import gettext_lazy as _
from .models import HireFormModel, CriticismSuggestionModel, ContactUsModel
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from extentions.utils import is_email, is_image


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


class CriticismSuggestionForm(forms.ModelForm):
    class Meta:
        model = CriticismSuggestionModel
        exclude = ['code', 'is_read', 'created']


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        exclude = ['is_read', 'created']

