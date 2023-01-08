from django.shortcuts import render, redirect
from hospital_contact.models import NotificationModel


# url: /
def home_page(request):
    return render(request, 'web/home.html', {})


# url: /read/notification/<notificationID>/
def read_notification(request, notificationID):
    if NotificationModel.objects.filter(id=notificationID).exists():
        notif = NotificationModel.objects.get(id=notificationID)
        notif.is_read = True
        notif.save()

        if request.GET.get('route'):
            return redirect(request.GET.get('route'))
        return redirect('website:home')
    return redirect('/404')