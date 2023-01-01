from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from hospital_doctor.models import DoctorModel, DoctorVacationModel
from django.contrib import messages
from .decorators import online_doctor_required
from .mixins import DoctorRequired
from . import forms


# url: /panel/doctor/vacation/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_doctor_required
def doctor_vacation_page(request):

    doctor = DoctorModel.objects.get(user=request.user)

    if request.method == 'POST':
        form = forms.DoctorVacationForm(request.POST or None)

        if form.is_valid():
            
            doctor.doctorvacationmodel_set.create(
                from_time=form.cleaned_data.get('from_time'),
                to_time=form.cleaned_data.get('to_time'),
                is_accepted=False,
            )

            form = forms.DoctorVacationForm()
            messages.success(request, _('درخواست شما با موفقیت ارسال شد. پس از بررسی تغییرات لازم روی نوبت دهی انجام میشود.'))
            return redirect('panel:doctor-vacation')

    else:
        form = forms.DoctorVacationForm()

    return render(request, 'panel/doctor/vacation.html', {
        'vacations': doctor.doctorvacationmodel_set.all(),
        'form': form
    })

