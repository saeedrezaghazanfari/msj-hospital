from django import template
from hospital_auth.models import SupporterModel, ContentProducerModel
from hospital_doctor.models import DoctorModel


register = template.Library()

@register.simple_tag
def get_user_labels(user):
    data = {
        'is_admin': False,
        'is_supporter': False,
        'is_contentproducer': False,
        'is_doctor': False,
    }
    if user.is_superuser:
        data['is_admin'] = True
    if DoctorModel.objects.filter(user=user).exists():
        data['is_doctor'] = True
    if SupporterModel.objects.filter(user=user).exists():
        data['is_supporter'] = True
    if ContentProducerModel.objects.filter(user=user).exists():
        data['is_contentproducer'] = True
    return data 