from django import forms
from hospital_auth.models import User
from django.utils.translation import gettext_lazy as _
from hospital_setting.models import InsuranceModel
from hospital_units.models import AppointmentTimeModel, LimitTurnTimeModel, AppointmentTipModel
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from extentions.utils import is_email, is_image


class EditInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile']
        widgets = {
            'first_name': forms.TextInput({'placeholder': _('نام خود را وارد کنید')}),
            'last_name': forms.TextInput({'placeholder': _('نام خانوادگی خود را وارد کنید')}),
            'email': forms.EmailInput({'placeholder': _('ایمیل خود را وارد کنید')}),
        }

    def validate_profile(self, value):
        if not is_image(value):
            raise forms.ValidationError(_('پسوند فایل مجاز نیست.'))
        return value

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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or len(email) == 0:
            raise forms.ValidationError(_('ایمیل خود را وارد کنید'))
        if not is_email(email):
            raise forms.ValidationError(_('الگوی ایمیل شما صحیح نیست'))
        return email


class LimitTurnTimeForm(forms.ModelForm):
    class Meta:
        model = LimitTurnTimeModel
        fields = ['hours', 'rules']

    def validate_hours(self, value):
        if value >= 168:
            raise forms.ValidationError(_('عدد ساعت نباید بزرگتر از 168 یا یک هفته باشد.'))
        if value < 6:
            raise forms.ValidationError(_('عدد ساعت نباید کمتر از 6 ساعت باشد.'))
        return value


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = InsuranceModel
        fields = ['title', 'img']

    def validate_title(self, value):
        if len(value) >= 90:
            raise forms.ValidationError(_('مقدار فیلد نباید بزرگتر از 90 کاراکتر باشد.'))
        if InsuranceModel.objects.filter(title=value).exists():
            raise forms.ValidationError(_('شما قبلا یک مقدار شبیه به این داده ثبت کرده اید.'))
        return value

    def validate_img(self, value):
        if not is_image(value):
            raise forms.ValidationError(_('پسوند فایل مجاز نیست.'))
        return value


class AppointmentTipForm(forms.ModelForm):
    class Meta:
        model = AppointmentTipModel
        fields = ['title', 'tips']

    def validate_title(self, value):
        if len(value) >= 90:
            raise forms.ValidationError(_('مقدار فیلد نباید بزرگتر از 90 کاراکتر باشد.'))
        if AppointmentTipModel.objects.filter(title=value).exists():
            raise forms.ValidationError(_('شما قبلا یک مقدار شبیه به این داده ثبت کرده اید.'))
        return value


class Time1AppointmentForm(forms.ModelForm):
    class Meta:
        model = AppointmentTimeModel
        fields = ['unit', 'doctor']


class Time2AppointmentForm(forms.ModelForm):
    date_from = forms.DateField(widget=forms.DateInput())
    date_to = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = AppointmentTimeModel
        fields = ['date_from', 'date_to', 'time_from', 'time_to', 'capacity', 'tip', 'tip_sms']

    def __init__(self, *args, **kwargs):
        super(Time2AppointmentForm, self).__init__(*args, **kwargs)
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
        from django.utils import timezone
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
        if date_from > date_to:
            raise forms.ValidationError(_('تاریخ مقصد نباید از تاریخ مبدا کوچکتر باشد.'))
        # if date_from < timezone.now().date:    #TODO
        #     raise forms.ValidationError(_('تاریخ نباید از زمان حال کوچکتر باشد.'))
        # if date_to < timezone.now().date:
        #     raise forms.ValidationError(_('تاریخ نباید از زمان حال کوچکتر باشد.'))
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