from django import template


register = template.Library()

@register.simple_tag
def get_user_labels(user):
    data = {
        'is_admin': False,
        'is_supporter': False,
        'is_contentproducer': False,
        'is_doctor': False,
    }
    return data 