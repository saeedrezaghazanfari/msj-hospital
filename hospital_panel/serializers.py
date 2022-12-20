from rest_framework import serializers
from hospital_units.models import LimitTurnTimeModel, AppointmentTipModel
from hospital_setting.models import InsuranceModel
from django.utils.translation import gettext_lazy as _
from extentions.utils import is_image


class LimitTurnTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitTurnTimeModel
        fields = ['to_hour', 'how_days_hour']

    def validate_to_hour(self, value):
        if value >= 25:
            raise serializers.ValidationError(_('عدد ساعت نباید بزرگتر از 24 باشد.'))
        if value <= 0:
            raise serializers.ValidationError(_('عدد ساعت نباید منفی باشد.'))
        return value

    def validate_how_days_hour(self, value):
        if value >= 7:
            raise serializers.ValidationError(_('مقدار این فیلد نباید بیشتر از یک هفته باشد.'))
        if value <= 0:
            raise serializers.ValidationError(_('مقدار این فیلد نباید منفی باشد.'))
        return value


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceModel
        fields = ['title', 'img']

    def validate_title(self, value):
        if len(value) >= 90:
            raise serializers.ValidationError(_('مقدار فیلد نباید بزرگتر از 90 کاراکتر باشد.'))
        if InsuranceModel.objects.filter(title=value).exists():
            raise serializers.ValidationError(_('شما قبلا یک مقدار شبیه به این داده ثبت کرده اید.'))
        return value

    def validate_img(self, value):
        if not is_image(value):
            raise serializers.ValidationError(_('پسوند فایل مجاز نیست.'))
        return value


class AppointmentTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentTipModel
        fields = ['title', 'tips']

    def validate_title(self, value):
        if len(value) >= 90:
            raise serializers.ValidationError(_('مقدار فیلد نباید بزرگتر از 90 کاراکتر باشد.'))
        if AppointmentTipModel.objects.filter(title=value).exists():
            raise serializers.ValidationError(_('شما قبلا یک مقدار شبیه به این داده ثبت کرده اید.'))
        return value

