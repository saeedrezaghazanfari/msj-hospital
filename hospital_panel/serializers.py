from rest_framework import serializers
from hospital_units.models import LimitTurnTimeModel
from django.utils.translation import gettext_lazy as _


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