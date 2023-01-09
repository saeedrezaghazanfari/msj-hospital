import calendar
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from hospital_units.models import (
    ExprimentResultModel,
)
from hospital_setting.models import PriceAppointmentModel, InsuranceModel
from hospital_doctor.models import DoctorModel, DoctorVacationModel, DegreeModel
from .decorators import experiment_required
from . import forms


# url: /panel/experiment/
@login_required(login_url=reverse_lazy('auth:signin'))
@experiment_required(login_url='/403')
def experiment_page(request):
    return render(request, 'panel/experiment/home.html', {})


# url: /panel/experiment/list/
@login_required(login_url=reverse_lazy('auth:signin'))
@experiment_required(login_url='/403')
def experiment_list_page(request):

    results = ExprimentResultModel.objects.all()    

    if request.method == 'POST':
        form = forms.ExprimentResultForm(request.POST, request.FILES or None)

        if form.is_valid():

            exp = ExprimentResultModel.objects.create(
                patient=form.cleaned_data.get('patient'),
                unit=form.cleaned_data.get('unit'),
                title=form.cleaned_data.get('title'),
                result=form.cleaned_data.get('result'),
                image=form.cleaned_data.get('image'),
                date=form.cleaned_data.get('date'),
                is_sent_sms=form.cleaned_data.get('is_sent_sms')
            )

            if exp.is_sent_sms:
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


