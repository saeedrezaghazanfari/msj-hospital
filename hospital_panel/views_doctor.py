from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from hospital_doctor.models import DoctorModel
from django.contrib import messages
from hospital_setting.models import InsuranceModel
from hospital_units.models import PatientTurnModel
from .decorators import online_doctor_required
# from .mixins import DoctorRequired
from . import forms


# url: /panel/doctor/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_doctor_required
def doctor_page(request):
    return render(request, 'panel/doctor/home.html', {})


# url: /panel/doctor/info/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_doctor_required
def doctor_info_page(request):

    doctor = None
    if DoctorModel.objects.filter(user=request.user, is_active=True).exists():
        doctor = DoctorModel.objects.get(user=request.user, is_active=True)

    if request.method == 'POST':
        form = forms.DoctorEditForm(request.POST or None)

        if form.is_valid():

            doctor.skill_title = form.cleaned_data.get('skill_title')
            doctor.degree = form.cleaned_data.get('degree')
            doctor.position_fa = form.cleaned_data.get('position_fa')
            doctor.position_en = form.cleaned_data.get('position_en')
            doctor.position_ar = form.cleaned_data.get('position_ar')
            doctor.position_ru = form.cleaned_data.get('position_ru')
            doctor.bio_fa = form.cleaned_data.get('bio_fa')
            doctor.bio_en = form.cleaned_data.get('bio_en')
            doctor.bio_ar = form.cleaned_data.get('bio_ar')
            doctor.bio_ru = form.cleaned_data.get('bio_ru')
            doctor.save()

            form = forms.DoctorEditForm()
            messages.success(request, _('اطلاعات شما با موفقیت تغییر یافت.'))
            return redirect('panel:doctor')

    else:
        form = forms.DoctorEditForm(instance=doctor)

    return render(request, 'panel/doctor/info.html', {
        'form': form
    })


# url: /panel/doctor/vacation/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_doctor_required
def doctor_vacation_page(request):

    doctor = DoctorModel.objects.get(user=request.user)

    if request.method == 'POST':
        form = forms.DoctorVacationForm(request.POST or None)

        if form.is_valid():
            
            doctor.doctorvacationmodel_set.create(
                from_date=form.cleaned_data.get('from_date'),
                to_date=form.cleaned_data.get('to_date'),
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


# url: /panel/doctor/work/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_doctor_required
def doctor_work_page(request):

    doctor = DoctorModel.objects.get(user=request.user)

    if request.method == 'POST':
        form = forms.DoctorWorkForm(request.POST or None)

        if form.is_valid():
            
            doctor.doctorworktimemodel_set.create(
                day_from=form.cleaned_data.get('day_from'),
                day_to=form.cleaned_data.get('day_to'),
                time_from=form.cleaned_data.get('time_from'),
                time_to=form.cleaned_data.get('time_to'),
            )

            form = forms.DoctorWorkForm()
            messages.success(request, _('زمان کاری شما با موفقیت ثبت شد.'))
            return redirect('panel:doctor-work')

    else:
        form = forms.DoctorWorkForm()

    return render(request, 'panel/doctor/work.html', {
        'works': doctor.doctorworktimemodel_set.all(),
        'form': form
    })


# url: /panel/doctor/insurances/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_doctor_required
def doctor_insurances_page(request):

    doctor = DoctorModel.objects.get(user=request.user)

    if request.method == 'POST':

        if request.POST.getlist('insurances') and len(request.POST.getlist('insurances')) > 0:

            doctor.insurances.clear()
            for item in request.POST.getlist('insurances'):
                doctor.insurances.add(InsuranceModel.objects.get(id=item))

            messages.success(request, _('بیمه های موردنظر با موفقیت برای شما ثبت شدند.'))
            return redirect('panel:doctor-insurances')

    return render(request, 'panel/doctor/insurances.html', {
        'insurances': InsuranceModel.objects.all(),
        'doctor': doctor
    })


# url: /panel/doctor/patients/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_doctor_required
def doctor_patients_page(request):

    patients = PatientTurnModel.objects.filter(
        is_paid=True,
        is_canceled=False,
        appointment__doctor=DoctorModel.objects.get(user=request.user),
        appointment__date__gt=timezone.now()
    ).all()

    return render(request, 'panel/doctor/patients.html', {
        'patients': patients
    })