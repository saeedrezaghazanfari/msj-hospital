from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CareersModel, HireFormModel
from . import forms


# url: /contact/careers/
def careers_page(request):

    return render(request, 'contact/recruitations.html', {
        'careers': CareersModel.objects.filter(is_active=True).all()
    })


# url: /contact/careers/info/<careerCode>/
def careers_info_page(request, careerCode):

    career = get_object_or_404(CareersModel, code=careerCode)
    form = forms.HireForm()


    if request.method == 'POST':
        form = forms.HireForm(request.POST, request.FILES or None)

        if form.is_valid():
            hireform = form.save(commit=False)
            hireform.career = career
            hireform.is_checked = False

            if HireFormModel.objects.filter(career=career, national_code=hireform.national_code).exists():
                messages.success(request, _('شما قبلا یک بار درخواست ارسال کرده اید.'))
                return redirect('contact:careers')
            else:
                hireform.save()

            # TODO send sms to hireform.phone

            messages.success(request, _('فرم با موفقیت ارسال شد. پس از بررسی با شما تماس گرفته خواهد شد.'))
            return redirect('website:home')

    else:
        form = forms.HireForm()

    return render(request, 'contact/recruitations-info.html', {
        'career': career,
        'form': form
    })