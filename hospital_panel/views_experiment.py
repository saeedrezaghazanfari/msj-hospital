import calendar
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from hospital_auth.models import PatientModel
from django.contrib import messages
from hospital_units.models import (
    ExprimentResultModel,
)
from extentions.utils import write_action
from .decorators import experiment_required
from . import forms


# url: /panel/experiment/
@login_required(login_url=reverse_lazy('auth:signin'))
@experiment_required(login_url=f'/{get_language()}/403')
def experiment_page(request):
    return render(request, 'panel/experiment/home.html', {})


# url: /panel/experiment/list/
@login_required(login_url=reverse_lazy('auth:signin'))
@experiment_required(login_url=f'/{get_language()}/403')
def experiment_list_page(request):

    results = ExprimentResultModel.objects.all()    

    if request.method == 'POST':
        form = forms.ExprimentResultForm(request.POST, request.FILES or None)

        if form.is_valid():
            exp = form.save()
            write_action(f'{request.user.username} User created a expriment result. experimentCode: {exp.code}', 'USER')

            # TODO send sms: send code of experiment to patient
            print(exp.code)

            messages.success(request, _('نتیجه ی آزمایش با موفقیت ثبت شد.'))
            return redirect('panel:experiment-list')

    else:
        form = forms.ExprimentResultForm()

    return render(request, 'panel/experiment/list.html', {
        'form': form,
        'results': results,
    })


# url: /panel/experiment/patient/
@login_required(login_url=reverse_lazy('auth:signin'))
@experiment_required(login_url=f'/{get_language()}/403')
def experiment_patient_page(request):

    if request.method == 'POST':
        form = forms.PatientForm(request.POST or None)

        if form.is_valid():

            if not PatientModel.objects.filter(username=form.cleaned_data.get('username')).exists():
                obj = form.save()
                write_action(f'{request.user.username} User Created a patient in Experiment panel. patientUsername: {obj.username}', 'USER')

            else:
                patient = PatientModel.objects.get(username=form.cleaned_data.get('username'))
                patient.first_name = form.cleaned_data.get('first_name')
                patient.last_name = form.cleaned_data.get('last_name')
                patient.phone = form.cleaned_data.get('phone')
                patient.gender = form.cleaned_data.get('gender')
                patient.age = form.cleaned_data.get('age')

                patient.save()
                write_action(f'{request.user.username} User Updated a patient in Experiment panel. patientUsername: {patient.username}', 'USER')
            
            messages.success(request, _('اطلاعات بیمار با موفقیت ثبت شد.'))
            return redirect('panel:experiment-list')

    else:
        form = forms.PatientForm()

    return render(request, 'panel/experiment/patient.html', {
        'form': form,
    })