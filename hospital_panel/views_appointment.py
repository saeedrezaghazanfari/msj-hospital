import calendar
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from hospital_units.models import (
    UnitModel, LimitTurnTimeModel, AppointmentTimeModel, 
    PatientTurnModel, AppointmentTipModel
)
from hospital_setting.models import PriceAppointmentModel, InsuranceModel
from hospital_doctor.models import DoctorModel, DoctorVacationModel, DegreeModel
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

    # create_form = forms.PriceAppointmentForm(request.POST or None)
    insurances = InsuranceModel.objects.all()
    degrees = DegreeModel.objects.all()

    list_data = []
    for insurance in insurances:
        for degree in degrees:
            if not PriceAppointmentModel.objects.filter(insurance=insurance, degree=degree).exists():
                list_data.append(
                    PriceAppointmentModel(
                        insurance=insurance,
                        degree=degree,
                        price=0,
                    )
                )
                
    for degree in degrees:
        if not PriceAppointmentModel.objects.filter(insurance=None, degree=degree).exists():
            list_data.append(
                PriceAppointmentModel(
                    insurance=None,
                    degree=degree,
                    price=0,
                )
            )

    PriceAppointmentModel.objects.bulk_create(list_data)

    prices = PriceAppointmentModel.objects.all()
    context = {
        'prices': prices,
    }

    if request.method == 'POST':
        price = int(request.POST.get('price'))
        data_id = request.POST.get('data')

        if price == 0:
            messages.error(request, _('مقدار مبلغ را وارد کنید.'))
            return redirect('panel:appointment-price')

        if price < 0:
            messages.error(request, _('مقدار این مبلغ نمیتواند منفی باشد.'))
            return redirect('panel:appointment-price')

        if price and data_id and PriceAppointmentModel.objects.filter(id=data_id).exists():
            appointment = PriceAppointmentModel.objects.get(id=data_id)
            appointment.price = price
            appointment.save()

        messages.success(request, _('تعرفه ی مورد نظر شما با موفقیت بروزرسانی شد.'))
        return redirect('panel:appointment-price')

    return render(request, 'panel/online-appointment/price-appointment.html', context)


# url: /panel/online-appointment/time/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_time_page(request):
    times = AppointmentTimeModel.objects.filter(date__gt=timezone.now()).all()
    return render(request, 'panel/online-appointment/time-appointment.html', {
        'times': times,
    })


# url: /panel/online-appointment/time/create/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_time_create1_page(request):

    create_form = forms.Time1AppointmentForm(request.POST or None)
    context = {
        'form': create_form,
    }

    if request.method == 'POST':
        if create_form.is_valid():
            
            unit = create_form.cleaned_data.get('unit')
            doctor = create_form.cleaned_data.get('doctor')
            if not doctor:
                return redirect('/404')

            context['form'] = forms.Time1AppointmentForm()
            if unit:
                return HttpResponseRedirect(reverse('panel:appointment-timep2', args=(unit.id, doctor.id)))
            return HttpResponseRedirect(reverse('panel:appointment-timep2', args=(0, doctor.id)))

    return render(request, 'panel/online-appointment/time-p1-appointment.html', context)


# url: /panel/online-appointment/time/create/<unitID>/<doctorId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_time_create2_page(request, unitID, doctorId):

    if int(unitID) != 0 and UnitModel.objects.filter(id=unitID).exists():
        unit = UnitModel.objects.get(id=unitID)
    elif int(unitID) == 0:
        unit = None
    elif not unitID:
        return redirect('/404')

    if doctorId and DoctorModel.objects.filter(id=doctorId).exists():
        doctor = DoctorModel.objects.get(id=doctorId)
    else:
        return redirect('/404')

    create_form = forms.Time2AppointmentForm(request.POST or None)
    context = {
        'form': create_form,
        'insurances': [insurance for insurance in doctor.insurances.all()]
    }

    if request.method == 'POST':
        if create_form.is_valid():

            date_from = create_form.cleaned_data.get('date_from')
            date_to = create_form.cleaned_data.get('date_to')
            range_date = date_range_list(date_from, date_to)
            insurances_list = request.POST.getlist('insurances')
            insurances_obj = []
            if len(insurances_list) > 0:
                for insurance in insurances_list:
                    if InsuranceModel.objects.filter(title=insurance).exists():
                        insurances_obj.append(InsuranceModel.objects.get(title=insurance))

            for date in range_date:
                day = calendar.day_name[date.weekday()].lower()
                
                time = AppointmentTimeModel.objects.create(
                    unit=unit,
                    doctor=doctor,
                    date=date,
                    day=day,
                    time_from=create_form.cleaned_data.get('time_from'),
                    time_to=create_form.cleaned_data.get('time_to'),
                    capacity=create_form.cleaned_data.get('capacity'),
                    reserved=0,
                    tip=create_form.cleaned_data.get('tip'),
                )
                # add insurances to queryset
                for item in insurances_obj:
                    time.insurances.add(item)

            context['form'] = forms.Time2AppointmentForm()
            messages.success(request, _('زمان نوبت دهی مورد نظر شما با موفقیت اضافه شد.'))
            return redirect('panel:appointment-time')

    return render(request, 'panel/online-appointment/time-p2-appointment.html', context)


# url: /panel/online-appointment/patient/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_patient_page(request):
    patients = PatientTurnModel.objects.all()
    return render(request, 'panel/online-appointment/patient.html', {
        'patients': patients
    })