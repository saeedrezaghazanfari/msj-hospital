from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib import messages
from extentions.utils import write_action
from .models import IPDModel
from . import forms


# url: /ipd/register/
def ipd_register_page(request):
    
    if request.method == 'POST':
        form = forms.IPDForm(request.POST, request.FILES or None)

        if form.is_valid():
            new_ipd = form.save(commit=False)

            country = request.POST.get('country')
            state = request.POST.get('state')
            city = request.POST.get('city')

            if not country or not state or not city:
                messages.error(request, _('باید مقادیر کشور استان و شهر را وارد کنید.'))
                return redirect('auth:ipd-register')
            
            if IPDModel.objects.filter(username=new_ipd.username, is_answered=False).exists():
                messages.error(request, _('شما قبلا یک فرم ارسال کرده اید. در صورتی که به آن فرم پاسخ داده شده باشد میتوانید فرم جدید ارسال کنید.'))
                return redirect('website:home')

            new_ipd.country = country
            new_ipd.state = state
            new_ipd.city = city

            new_ipd.save()
            write_action(f'user via {new_ipd.username} nationalCode/passport sent ipd form.', 'ANONYMOUS')

            if new_ipd.email:
                # TODO send email to new_ipd.email
                ...
            # TODO send sms to new_ipd.phone

            messages.success(request, _('فرم شما با موفقیت ارسال شد. تیم پزشکی ما در اسرع وقت بررسی خواهد کرد.'))
            return redirect('website:home')

    else:
        form = forms.IPDForm()

    return render(request, 'ipd/register.html', {
        'form': form
    })
