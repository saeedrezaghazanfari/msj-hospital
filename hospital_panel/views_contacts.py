from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from hospital_contact.models import (
    CareersModel, HireFormModel, CriticismSuggestionModel, ContactUsModel
)
from extentions.utils import write_action
from .decorators import contact_required
from . import forms


# url: /panel/contact/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required(login_url=f'/{get_language()}/403')
def contact_page(request):
    return render(request, 'panel/contacts/home.html', {})


# url: /panel/contact/careers/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required(login_url=f'/{get_language()}/403')
def contact_careers_page(request):

    if request.method == 'POST':
        form = forms.CareersForm(request.POST, request.FILES or None)

        if form.is_valid():

            obj = form.save()
            write_action(f'{request.user.username} User created a career in Contact panel. careerCode: {obj.code}', 'USER')

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
@contact_required(login_url=f'/{get_language()}/403')
def contact_career_edit_page(request, careerCode):

    career = get_object_or_404(CareersModel, code=careerCode)

    if request.method == 'POST':
        form = forms.CareersForm(request.POST, request.FILES or None, instance=career)

        if form.is_valid():

            form.save()
            write_action(f'{request.user.username} User edited a career in Contact panel. careerCode: {careerCode}', 'USER')

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
@contact_required(login_url=f'/{get_language()}/403')
def contact_recruitations_page(request):
    return render(request, 'panel/contacts/recruitations.html', {
        'checked': HireFormModel.objects.filter(is_checked=True).all(),
        'unchecked': HireFormModel.objects.filter(is_checked=False).all(),
    })


# url: /panel/contact/recruitations/info/<hireId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required(login_url=f'/{get_language()}/403')
def contact_recruitations_info_page(request, hireId):

    hire = get_object_or_404(HireFormModel, id=hireId)

    if request.method == 'POST' and request.POST.get('check_hire'):
        hire.is_checked = True
        hire.save()

        write_action(f'{request.user.username} User checked a user Recruitations in Contact panel. hireId: {hireId}', 'USER')

        messages.success(request, _('فرم استخدامی بررسی شد.'))
        return redirect('panel:contact-recruitations')

    return render(request, 'panel/contacts/recruitations-info.html', {
        'hire': hire,
    })


# url: /panel/contact/suggestions/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required(login_url=f'/{get_language()}/403')
def contact_suggestions_page(request):

    return render(request, 'panel/contacts/suggestions.html', {
        'unread_suggestions': CriticismSuggestionModel.objects.filter(is_read=False).all(),
        'read_suggestions': CriticismSuggestionModel.objects.filter(is_read=True).all(),
    })


# url: /panel/contact/suggestions/info/<suggestionCode>/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required(login_url=f'/{get_language()}/403')
def contact_suggestions_info_page(request, suggestionCode):

    suggestion = get_object_or_404(CriticismSuggestionModel, code=suggestionCode)

    if request.method == 'POST' and request.POST.get('read_suggestion'):
        suggestion.is_read = True
        suggestion.save()

        write_action(f'{request.user.username} User checked a user Suggestions in Contact panel. suggestionCode: {suggestionCode}', 'USER')

        messages.success(request, _('رکورد مورد نظر خوانده شد.'))
        return redirect('panel:contact-suggestions')

    return render(request, 'panel/contacts/suggestions-info.html', {
        'suggestion': suggestion,
    })


# url: /panel/contact/contacts/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required(login_url=f'/{get_language()}/403')
def contact_contacts_page(request):

    return render(request, 'panel/contacts/contacts.html', {
        'unread_contacts': ContactUsModel.objects.filter(is_read=False).all(),
        'read_contacts': ContactUsModel.objects.filter(is_read=True).all(),
    })


# url: /panel/contact/contacts/info/<contactId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@contact_required(login_url=f'/{get_language()}/403')
def contact_contacts_info_page(request, contactId):

    contact = get_object_or_404(ContactUsModel, id=contactId)

    if request.method == 'POST' and request.POST.get('read_contact'):
        contact.is_read = True
        contact.save()

        write_action(f'{request.user.username} User checked a user ContactsUs form in Contact panel. contactId: {contactId}', 'USER')

        messages.success(request, _('رکورد مورد نظر خوانده شد.'))
        return redirect('panel:contact-contacts')

    return render(request, 'panel/contacts/contacts-info.html', {
        'contact': contact,
    })
