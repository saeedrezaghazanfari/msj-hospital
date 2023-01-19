from django import template
from hospital_contact.models import NotificationModel


register = template.Library()


@register.simple_tag
def get_user_notif(username):

    if username.is_authenticated:
        notifications = NotificationModel.objects.filter(
            user=username,
            is_read=False,
            is_published=True
        ).all()
        
        return notifications
    return []