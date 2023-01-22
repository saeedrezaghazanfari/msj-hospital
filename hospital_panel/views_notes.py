from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .decorators import note_required
from hospital_blog.models import MedicalNoteModel
from . import forms


# url: /panel/notes
@login_required(login_url=reverse_lazy('auth:signin'))
@note_required
def notes_page(request):

    if request.method == 'POST':
        form = forms.MedicalNoteForm(request.POST or None)

        if form.is_valid():

            form.save()
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
@note_required
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
        'notes': MedicalNoteModel.objects.all(),
        'form': form,
    })