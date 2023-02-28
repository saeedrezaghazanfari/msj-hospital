from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from extentions.utils import write_action
from hospital_setting.models import SettingModel
from .models import (
    CareersModel, HireFormModel, CriticismSuggestionModel, 
    ContactUsModel, PatientSightModel, BeneficiaryCommentModel, 
    PeopleAidModel,
)
from . import forms


# url: /contact/careers/
def careers_page(request):

    return render(request, 'contact/recruitations.html', {
        'careers': CareersModel.objects.filter(is_active=True).all()
    })


# url: /contact/careers/info/<careerCode>/
def careers_info_page(request, careerCode):

    career = get_object_or_404(CareersModel, code=careerCode)

    if request.method == 'POST':
        form = forms.HireForm(request.POST, request.FILES or None)

        if form.is_valid():
            hireform = form.save(commit=False)
            hireform.career = career
            hireform.is_checked = False

            if HireFormModel.objects.filter(career=career, national_code=hireform.national_code).exists():
                messages.warning(request, _('شما قبلا یک بار درخواست ارسال کرده اید.'))
                return redirect('contact:careers')
            else:
                hireform.save()
                write_action(f'user via {hireform.national_code} NationalCode sent a hire form. hireformId: {hireform.id}', 'ANONYMOUS')

            # TODO send sms to hireform.phone

            messages.success(request, _('فرم با موفقیت ارسال شد. پس از بررسی با شما تماس گرفته خواهد شد.'))
            return redirect('website:home')

    else:
        form = forms.HireForm()

    return render(request, 'contact/recruitations-info.html', {
        'career': career,
        'form': form
    })


# url: /contact/suggestions/
def suggestions_page(request):

    if request.method == 'POST':
        form = forms.CriticismSuggestionForm(request.POST or None)

        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.is_read = False

            if CriticismSuggestionModel.objects.filter(national_code=suggestion.national_code, is_read=False).exists():
                messages.warning(request, _('فرم قبلی که ارسال کرده اید هنوز بررسی نشده است.'))
                return redirect('website:home')
            else:
                suggestion.save()
                write_action(f'user via {suggestion.national_code} NationalCode sent a suggestion. suggestionCode: {suggestion.code}', 'ANONYMOUS')

            # TODO send sms to suggestion.phone

            messages.success(request, _('ممنون از تبادلات شما. در اسرع وقت بررسی خواهد شد!'))
            return redirect('website:home')

    else:
        form = forms.CriticismSuggestionForm()

    return render(request, 'contact/suggestions.html', {
        'form': form
    })



# url: /contact/contactus/
def contactus_page(request):

    if request.method == 'POST':
        form = forms.ContactUsForm(request.POST or None)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.is_read = False

            if ContactUsModel.objects.filter(email=contact.email, phone=contact.phone, is_read=False).exists():
                messages.warning(request, _('فرم قبلی که ارسال کرده اید هنوز بررسی نشده است.'))
                return redirect('website:home')
            else:
                contact.save()
                write_action(f'user via {contact.phone} Phone sent a contact us form. contactId: {contact.id}', 'ANONYMOUS')

            # TODO send sms to contact.phone

            messages.success(request, _('ممنون از تبادلات شما. در اسرع وقت بررسی خواهد شد!'))
            return redirect('website:home')

    else:
        form = forms.ContactUsForm()    

    return render(request, 'contact/contactus.html', {
        'form': form
    })


# url: /contact/info/
def info_page(request):

    return render(request, 'contact/info.html', {
        'phones': SettingModel.objects.first().phone if SettingModel.objects.exists() else None,
    })


# url: /contact/beneficiaries-comments/
def beneficiaries_comments_page(request):

    return render(request, 'contact/beneficiaries-comments.html', {
        'comments': BeneficiaryCommentModel.objects.all()[:6],
    })


# url: /contact/patients-comments/
def patients_comments_page(request):

    return render(request, 'contact/patients-comments.html', {
        'comments': PatientSightModel.objects.all()[:6],
    })


# url: /contact/people-aids/
def people_aids_page(request):

    return render(request, 'contact/people-aids.html', {
        'aids': PeopleAidModel.objects.all(),
    })
