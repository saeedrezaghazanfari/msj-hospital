from django import template
from hospital_doctor.models import DoctorModel, TitleSkillModel, DegreeModel


register = template.Library()


@register.simple_tag
def doctors_list():
    doctors = DoctorModel.objects.filter(is_active=True).all()
    return doctors


@register.simple_tag
def skill_list():
    skills = TitleSkillModel.objects.all()
    return skills


@register.simple_tag
def degree_list():
    degrees = DegreeModel.objects.all()
    return degrees