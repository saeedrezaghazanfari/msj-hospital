from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .decorators import note_required
from hospital_blog.models import MedicalNoteModel, SMSTextModel
from hospital_auth.models import PatientModel, User
from hospital_ipd.models import IPDModel
from extentions.utils import write_action
from . import forms


# url: /panel/notes
@login_required(login_url=reverse_lazy('auth:signin'))
@note_required(login_url=f'/{get_language()}/403')
def notes_page(request):

    if request.method == 'POST':
        form = forms.MedicalNoteForm(request.POST or None)

        if form.is_valid():

            object = form.save()
            write_action(f'{request.user.username} User wrote a note. noteId: {object.id}', 'USER')

            messages.success(request, _('نوت پزشکی مورد نظر شما ثبت شد.'))
            return redirect('panel:notes-list')

    else:
        form = forms.MedicalNoteForm()
            
    return render(request, 'panel/notes/list.html', {
        'notes': MedicalNoteModel.objects.all(),
        'form': form,
    })


# url: /panel/notes/<noteId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@note_required(login_url=f'/{get_language()}/403')
def notes_edit_page(request, noteId):

    note = get_object_or_404(MedicalNoteModel, id=noteId)

    if request.method == 'POST':
        form = forms.MedicalNoteForm(request.POST or None, instance=note)

        if form.is_valid():

            form.save()
            messages.success(request, _('نوت پزشکی مورد نظر شما ویرایش شد.'))
            return redirect('panel:notes-list')

    else:
        form = forms.MedicalNoteForm(instance=note)
            
    return render(request, 'panel/notes/edit.html', {
        'form': form,
    })


def send_sms_to_users(object):

    society = list()

    if object.receivers == 'patients':
        society = PatientModel.objects.all()

    elif object.receivers == 'patientsipd':
        society = IPDModel.objects.all()

    elif object.receivers == 'doctors':
        society = User.objects.filter(is_doctor_manager=True).all()

    elif object.receivers == 'bloggers':
        society = User.objects.filter(is_blog_manager=True).all()

    elif object.receivers == 'news':
        society = User.objects.filter(is_news_manager=True).all()

    elif object.receivers == 'lab':
        society = User.objects.filter(is_expriment_manager=True).all()

    elif object.receivers == 'appointment':
        society = User.objects.filter(is_appointment_manager=True).all()

    elif object.receivers == 'contacts':
        society = User.objects.filter(is_contact_manager=True).all()

    elif object.receivers == 'ipdmanager':
        society = User.objects.filter(is_ipd_manager=True).all()

    elif object.receivers == 'all':
        society = User.objects.all()

    if society:

        phones_list = list()

        for item in society:
            if not item.phone in phones_list:
                phones_list.append(item.phone)

        #TODO send sms to phones_list

        object.is_sent_sms = True
        object.save()


# url: /panel/notes/sms/list/
@login_required(login_url=reverse_lazy('auth:signin'))
@note_required(login_url=f'/{get_language()}/403')
def notes_smslist_page(request):

    if request.method == 'POST':
        form = forms.SMSTextForm(request.POST or None)

        if form.is_valid():

            object = form.save()

            if not object.is_sent_sms and object.is_sent:
                send_sms_to_users(object=object)
                
            write_action(f'{request.user.username} User wrote a sms. smsId: {object.id}', 'USER')

            messages.success(request, _('پیامک مورد نظر شما ثبت شد.'))
            return redirect('panel:notes-smslist')

    else:
        form = forms.SMSTextForm()
            
    return render(request, 'panel/notes/sms-list.html', {
        'smss': SMSTextModel.objects.all(),
        'form': form,
    })


# url: /panel/notes/sms/<smsId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@note_required(login_url=f'/{get_language()}/403')
def notes_smsinfo_page(request, smsId):

    sms = get_object_or_404(SMSTextModel, id=smsId)

    if request.method == 'POST':
        form = forms.SMSTextForm(request.POST or None, instance=sms)

        if form.is_valid():

            object = form.save(commit=False)

            if not object.is_sent_sms and object.is_sent:
                send_sms_to_users(object=object)

            messages.success(request, _('پیامک مورد نظر شما ویرایش شد.'))
            return redirect('panel:notes-smslist')

    else:
        form = forms.SMSTextForm(instance=sms)
            
    return render(request, 'panel/notes/sms-info.html', {
        'form': form,
        'sms': sms
    })