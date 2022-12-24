import calendar
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from hospital_units.models import LimitTurnTimeModel, AppointmentTimeModel, PatientTurnModel, AppointmentTipModel
from hospital_setting.models import PriceAppointmentModel, InsuranceModel
from hospital_doctor.models import DoctorModel, DoctorVacationModel
from extentions.utils import date_range_list
from .decorators import online_appointment_required
from . import forms


# url: /panel/online-appointment
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url='/403')
def online_appointment_page(request):
    return render(request, 'panel/online-appointment/home.html', {})


# url: /panel/online-appointment/limit-time/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_limit_time_page(request):
    form = forms.LimitTurnTimeForm(request.POST or None)
    limit_time = LimitTurnTimeModel.objects.last()
    context = {
        'limit_time': limit_time,
        'form': form
    }

    if request.method == 'POST':
        if form.is_valid():
            if LimitTurnTimeModel.objects.exists():
                LimitTurnTimeModel.objects.all().delete()

            form.save()
            context['form'] = forms.LimitTurnTimeForm()
            messages.success(request, _('حد زمانی نوبت اینترنتی با موفقیت تنظیم شد.'))
            return redirect('panel:appointment-limittime')
    
    return render(request, 'panel/online-appointment/limittime.html', context)


# url: /panel/online-appointment/insurances/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_insurances_page(request):
    form = forms.InsuranceForm(request.POST, request.FILES or None)
    insurances = InsuranceModel.objects.all()
    context = {
        'form': form,
        'insurances': insurances
    }
    if request.method == 'POST':
        if form.is_valid():

            form.save()
            context['form'] = forms.InsuranceForm()
            messages.success(request, _('بیمه ی مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-insurances')

    return render(request, 'panel/online-appointment/insurances.html', context)


# url: /panel/online-appointment/tips/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_tips_page(request):
    form = forms.AppointmentTipForm(request.POST or None)
    tips = AppointmentTipModel.objects.all()
    context = {
        'form': form,
        'tips': tips
    }
    if request.method == 'POST':
        if form.is_valid():

            form.save()
            context['form'] = forms.AppointmentTipForm()
            messages.success(request, _('نکته ی نوبت دهی مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-tips')

    return render(request, 'panel/online-appointment/tips.html', context)


# url: /panel/online-appointment/doctor/list/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_doctorlist_page(request):
    doctors = DoctorModel.objects.filter(is_active=True).all()

    for doctor in doctors:
        doctor.have_not_accecpted_vac = False
        if doctor.doctorvacationmodel_set.filter(is_accepted=False).exists():
            doctor.have_not_accecpted_vac = True

    return render(request, 'panel/online-appointment/doctor-list.html', {
        'doctors': doctors
    })


# url: /panel/online-appointment/doctor/<int:medicalCode>/times/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_doctorlist_time_page(request, medicalCode):

    if medicalCode and DoctorModel.objects.filter(medical_code=medicalCode, is_active=True).exists():
    
        doctor = DoctorModel.objects.get(medical_code=medicalCode, is_active=True)
        works = doctor.doctorworktimemodel_set.all()
        vacations = doctor.doctorvacationmodel_set.all()

        # update vacation of doctor
        if request.GET.get('vid') and DoctorVacationModel.objects.filter(id=request.GET.get('vid')).exists():
            doc_vac = DoctorVacationModel.objects.get(id=request.GET.get('vid'))
            doc_vac.is_accepted=True
            doc_vac.save()

        return render(request, 'panel/online-appointment/doctor-time.html', {
            'doctor': doctor,
            'works': works,
            'vacations': vacations,
        })
    return redirect('/404')


# url: /panel/online-appointment/price/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_price_page(request):

    create_form = forms.PriceAppointmentForm(request.POST or None)
    prices = PriceAppointmentModel.objects.all()
    context = {
        'prices': prices,
        'form': create_form,
    }

    if request.method == 'POST':
        if create_form.is_valid():
            create_form.save()
            context['form'] = forms.PriceAppointmentForm()

            messages.success(request, _('تعرفه ی مورد نظر شما با موفقیت اضافه شد.'))
            return redirect('panel:appointment-price')

    return render(request, 'panel/online-appointment/price-appointment.html', context)


# url: /panel/online-appointment/time/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_time_page(request):

    create_form = forms.TimeAppointmentForm(request.POST or None)
    times = AppointmentTimeModel.objects.all()
    context = {
        'times': times,
        'form': create_form,
    }

    if request.method == 'POST':
        if create_form.is_valid():

            date_from = create_form.cleaned_data.get('date_from')
            date_to = create_form.cleaned_data.get('date_to')
            range_date = date_range_list(date_from, date_to)
            time_list = []

            for date in range_date:
                day = calendar.day_name[date.weekday()].lower()
                
                time_list.append(
                    AppointmentTimeModel(
                        unit=create_form.cleaned_data.get('unit'),
                        doctor=create_form.cleaned_data.get('doctor'),
                        date=date,
                        day=day,
                        time_from=create_form.cleaned_data.get('time_from'),
                        time_to=create_form.cleaned_data.get('time_to'),
                        price=create_form.cleaned_data.get('price'),
                        capacity=create_form.cleaned_data.get('capacity'),
                        reserved=0,
                        tip=create_form.cleaned_data.get('tip'),
                    )
                )

            AppointmentTimeModel.objects.bulk_create(time_list)
            context['form'] = forms.TimeAppointmentForm()
            messages.success(request, _('زمان نوبت دهی مورد نظر شما با موفقیت اضافه شد.'))
            return redirect('panel:appointment-time')

    return render(request, 'panel/online-appointment/time-appointment.html', context)


# url: /panel/online-appointment/patient/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_patient_page(request):
    patients = PatientTurnModel.objects.all()
    return render(request, 'panel/online-appointment/patient.html', {
        'patients': patients
    })