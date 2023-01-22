from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from hospital_contact.models import CareersModel, HireFormModel
from .decorators import contact_required
from . import forms


# url: /panel/contact/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required
def contact_page(request):
    return render(request, 'panel/contacts/home.html', {})


# url: /panel/contact/careers/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required
def contact_careers_page(request):

    if request.method == 'POST':
        form = forms.CareersForm(request.POST, request.FILES or None)

        if form.is_valid():
            form.save()
            messages.success(request, _('موقعیت شغلی مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:contact-careers')

    else:
        form = forms.CareersForm()

    return render(request, 'panel/contacts/careers.html', {
        'form': form,
        'careers': CareersModel.objects.all(),
    })


# url: /panel/contact/careers/edit/<careerCode>/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required
def contact_career_edit_page(request, careerCode):

    career = get_object_or_404(CareersModel, code=careerCode)

    if request.method == 'POST':
        form = forms.CareersForm(request.POST, request.FILES or None, instance=career)

        if form.is_valid():
            form.save()
            messages.success(request, _('موقعیت شغلی مورد نظر با موفقیت ویرایش شد.'))
            return redirect('panel:contact-careers')

    else:
        form = forms.CareersForm(instance=career)

    return render(request, 'panel/contacts/careers-edit.html', {
        'form': form,
        'careers': CareersModel.objects.all(),
    })


# url: /panel/contact/recruitations/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required
def contact_recruitations_page(request):
    return render(request, 'panel/contacts/recruitations.html', {
        'checked': HireFormModel.objects.filter(is_checked=True).all(),
        'unchecked': HireFormModel.objects.filter(is_checked=False).all(),
    })


# url: /panel/contact/recruitations/info/<hireId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required
def contact_recruitations_info_page(request, hireId):

    hire = get_object_or_404(HireFormModel, id=hireId)

    if request.method == 'POST' and request.POST.get('check_hire'):
        hire.is_checked = True
        hire.save()

        messages.success(request, _('فرم استخدامی بررسی شد.'))
        return redirect('panel:contact-recruitations')

    return render(request, 'panel/contacts/recruitations-info.html', {
        'hire': hire,
    })