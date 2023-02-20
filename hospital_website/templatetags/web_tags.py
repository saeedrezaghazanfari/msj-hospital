from django import template
from hospital_blog.models import MedicalNoteModel
from hospital_units.models import UnitModel


register = template.Library()

@register.simple_tag
def doctor_notes():
    data = MedicalNoteModel.objects.filter(is_active=True).all()[:6]
    if data:
        return data
    return None

@register.simple_tag
def list_clinics():
    data = UnitModel.objects.filter(subunit__category='medical', subunit__title_fa='درمانگاه').all()
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
    data = UnitModel.objects.filter(subunit__category='medical').all()
    if data:
        return data
    return None

