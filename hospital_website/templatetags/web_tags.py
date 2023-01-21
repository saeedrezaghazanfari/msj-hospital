from django import template
from hospital_blog.models import MedicalNoteModel


register = template.Library()

@register.simple_tag
def doctor_notes():
    notes = MedicalNoteModel.objects.filter(is_active=True).all()[:6]
    if notes:
        return notes
    return None
