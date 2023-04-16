from django.db.models import Q
from django import template
from hospital_blog.models import MedicalNoteModel
from hospital_units.models import UnitModel
from hospital_setting.models import SettingModel


register = template.Library()

@register.simple_tag
def doctor_notes():
    data = MedicalNoteModel.objects.filter(is_active=True).all()[:6]
    if data:
        return data
    return None

@register.simple_tag
def list_paraclinics():
    data = UnitModel.objects.filter(subunit__category='paraclinic').all()
    if data:
        return data
    return None

@register.simple_tag
def list_officials():
    data = UnitModel.objects.filter(subunit__category='official').all()
    if data:
        return data
    return None

@register.simple_tag
def list_medicals():
    data = UnitModel.objects.filter(~Q(subunit__title_fa='درمانگاه'), subunit__category='medical').all()
    if data:
        return data
    return None

@register.simple_tag
def footer_data():
    data = SettingModel.objects.first()
    if data:
        return data
    return None
