import calendar
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from hospital_doctor.models import TitleSkillModel
from hospital_units.models import (
    UnitModel, LimitTurnTimeModel, AppointmentTimeModel, 
    PatientTurnModel, AppointmentTipModel, SubUnitModel
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

    if request.method == 'POST':
        form = forms.LimitTurnTimeForm(request.POST or None)

        if form.is_valid():
            if LimitTurnTimeModel.objects.exists():
                LimitTurnTimeModel.objects.all().delete()

            form.save()
            form = forms.LimitTurnTimeForm()
            messages.success(request, _('حد زمانی نوبت اینترنتی با موفقیت تنظیم شد.'))
            return redirect('panel:appointment-limittime')
    
    else:
        form = forms.LimitTurnTimeForm()

    return render(request, 'panel/online-appointment/limittime.html', {
        'limit_time': LimitTurnTimeModel.objects.last(),
        'form': form
    })


# url: /panel/online-appointment/insurances/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_insurances_page(request):

    if request.method == 'POST':
        form = forms.InsuranceForm(request.POST, request.FILES or None)

        if form.is_valid():
            form.save()
            form = forms.InsuranceForm()
            messages.success(request, _('بیمه ی مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-insurances')

    else:
        form = forms.InsuranceForm()

    return render(request, 'panel/online-appointment/insurances.html', {
        'form': form,
        'insurances': InsuranceModel.objects.all()
    })


# url: /panel/online-appointment/tips/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_tips_page(request):

    if request.method == 'POST':
        form = forms.AppointmentTipForm(request.POST or None)

        if form.is_valid():
            form.save()
            form = forms.AppointmentTipForm()
            messages.success(request, _('نکته ی نوبت دهی مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-tips')

    else:
        form = forms.AppointmentTipForm()

    return render(request, 'panel/online-appointment/tips.html', {
        'form': form,
        'tips': AppointmentTipModel.objects.all()
    })


# url: /panel/online-appointment/skill/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_skilltitle_page(request):

    if request.method == 'POST':
        form = forms.SkillForm(request.POST or None)

        if form.is_valid():
            form.save()
            form = forms.SkillForm()
            messages.success(request, _('تخصص مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-skill')

    else:
        form = forms.SkillForm()

    return render(request, 'panel/online-appointment/skill.html', {
        'form': form,
        'skills': TitleSkillModel.objects.all()
    })


# url: /panel/online-appointment/degree/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_degree_page(request):

    if request.method == 'POST':
        form = forms.DegreeForm(request.POST or None)

        if form.is_valid():
            form.save()
            form = forms.DegreeForm()
            messages.success(request, _('مدرک مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-degree')

    else:
        form = forms.DegreeForm()

    return render(request, 'panel/online-appointment/degree.html', {
        'form': form,
        'degrees': DegreeModel.objects.all()
    })


# url: /panel/online-appointment/unit/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_unit_page(request):

    if request.method == 'POST':
        form = forms.UnitForm(request.POST, request.FILES or None)

        if form.is_valid():
            form.save()
            form = forms.UnitForm()
            messages.success(request, _('بخش مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-unit')

    else:
        form = forms.UnitForm()

    return render(request, 'panel/online-appointment/unit.html', {
        'form': form,
        'units': UnitModel.objects.all()
    })


# url: /panel/online-appointment/subunit/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_subunit_page(request):

    paraclinics = ['فیزیوتراپی', 'آزمایشگاه', 'پاتولوژی', 'تصویر برداری']
    medicals = ['دیالیز', 'IPD', 'اورزانس', 'درمانگاه', 'قلب', 'ccu', 'آنژیوگرافی', 'اتاق عمل مرکزی', 'اتاق عمل قلب باز', 'CSR', 'ICU بزرگسال', 'جراحی زنان', 'زنان و زایمان', 'جراحی مردان', 'اطفال و نوزادان یا NICU']
    officials = ['مدیریت و ریاست', 'حسابداری', 'منابع انسانی', 'اسناد پزشکی', 'ترخیص و پذیرش', 'آی تی', 'تاسیسات', 'لنژری', 'آشپزحانه', 'تجهیزات پزشگی', 'بهداشت حرفه ای', 'بهداشت محیط', 'بهبود کیفیت', 'نگهبانی', 'مددکاری', 'انبارها', 'زباله سوز', 'کمیته']

    paraclinics_list = []
    medicals_list = []
    officials_list = []

    for item in paraclinics:
        if not SubUnitModel.objects.filter(category='paraclinic', title=item).exists():
            paraclinics_list.append(
                SubUnitModel(category='paraclinic', title=item)
            )

    for item in medicals:
        if not SubUnitModel.objects.filter(category='medical', title=item).exists():
            medicals_list.append(
                SubUnitModel(category='medical', title=item)
            )

    for item in officials:
        if not SubUnitModel.objects.filter(category='official', title=item).exists():
            officials_list.append(
                SubUnitModel(category='official', title=item)
            )

    if len(paraclinics_list) > 0:
        SubUnitModel.objects.bulk_create(paraclinics_list)
    if len(medicals_list) > 0:
        SubUnitModel.objects.bulk_create(medicals_list)
    if len(officials_list) > 0:
        SubUnitModel.objects.bulk_create(officials_list)

    if request.method == 'POST':
        form = forms.SubUnitForm(request.POST or None)

        if form.is_valid():
            form.save()
            form = forms.SubUnitForm()
            messages.success(request, _('زیربخش مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-subunit')

    else:
        form = forms.SubUnitForm()

    return render(request, 'panel/online-appointment/subunit.html', {
        'form': form,
        'subunits': SubUnitModel.objects.all()
    })


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


# url: /panel/online-appointment/doctor/create/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_doctorcreate_page(request):

    if request.method == 'POST':
        form = forms.DoctorForm(request.POST or None)

        if form.is_valid():
            ...

    else:
        form = forms.DoctorForm()

    return render(request, 'panel/online-appointment/doctor-create.html', {
        'form': form
    })


# url: /panel/online-appointment/doctor/<doctorId>/times/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_doctorlist_time_page(request, doctorId):

    try:
        DoctorModel.objects.filter(id=doctorId, is_active=True).exists()
    except:
        return redirect('/404')

    if doctorId and DoctorModel.objects.filter(id=doctorId, is_active=True).exists():

        doctor = DoctorModel.objects.get(id=doctorId, is_active=True)
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
    
    if request.GET.get('type') == 'doctors':
        times = AppointmentTimeModel.objects.filter(
            unit=None,
            date__gt=timezone.now()
        ).all()

    if request.GET.get('type') == 'labs':
        times = AppointmentTimeModel.objects.filter(
            unit__subunit__category='paraclinic',
            unit__subunit__title='آزمایشگاه',
            date__gt=timezone.now()
        ).all()

    if request.GET.get('type') == 'imaging':
        times = AppointmentTimeModel.objects.filter(
            unit__subunit__category='paraclinic',
            unit__subunit__title='تصویربرداری',
            date__gt=timezone.now()
        ).all()

    else:
        times = AppointmentTimeModel.objects.filter(
            date__gt=timezone.now()
        ).all()
    
    return render(request, 'panel/online-appointment/time-appointment.html', {
        'times': times,
    })


# url: /panel/online-appointment/time/<appointmentID>/edit/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_time_edit_page(request, appointmentID):

    if not appointmentID or not AppointmentTimeModel.objects.filter(id=appointmentID).exists():
        return redirect('/404')

    appointment = AppointmentTimeModel.objects.get(id=appointmentID)

    if request.method == 'POST':
        form = forms.AllAppointmentForm(request.POST or None)

        if form.is_valid():

            if form.cleaned_data.get('unit'):
                appointment.unit = form.cleaned_data.get('unit')
            else:
                appointment.unit = None
            if request.POST.getlist('insurances') and len(request.POST.getlist('insurances')) > 0:
                appointment.insurances.clear()
                for item in request.POST.getlist('insurances'):
                    appointment.insurances.add(InsuranceModel.objects.get(title=item))
            if form.cleaned_data.get('time_from'):
                appointment.time_from = form.cleaned_data.get('time_from')
            if form.cleaned_data.get('time_to'):
                appointment.time_to = form.cleaned_data.get('time_to')
            if form.cleaned_data.get('capacity'):
                appointment.capacity = form.cleaned_data.get('capacity')
            if form.cleaned_data.get('tip'):
                appointment.tip = form.cleaned_data.get('tip')
            if form.cleaned_data.get('tip_sms'):
                appointment.tip_sms = form.cleaned_data.get('tip_sms')
            appointment.save()

            form = forms.AllAppointmentForm()
            messages.success(request, _('زمان نوبت دهی موردنظر با موفقیت تغییر یافت.'))
            return redirect('panel:appointment-time')

    else:
        form = forms.AllAppointmentForm(instance=appointment)

    times = AppointmentTimeModel.objects.filter(date__gt=timezone.now()).all()
    return render(request, 'panel/online-appointment/edit-time-appointment.html', {
        'times': times,
        'form': form,
        'appointment': appointment,
        'insurances': [insurance for insurance in appointment.doctor.insurances.all()]
    })


# url: /panel/online-appointment/time/create/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_time_create0_page(request):

    if request.method == 'POST':
        form = forms.Time0AppointmentForm(request.POST or None)

        if form.is_valid():
            unit = form.cleaned_data.get('unit')
            form = forms.Time0AppointmentForm()

            if unit:
                return HttpResponseRedirect(reverse('panel:appointment-timep1', args=(unit.id,)))
            return HttpResponseRedirect(reverse('panel:appointment-timep1', args=('none',)))
    else:
        form = forms.Time0AppointmentForm()

    return render(request, 'panel/online-appointment/time-p0-appointment.html', {
        'form': form,
    })


# url: /panel/online-appointment/time/create/<unitID>/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_time_create1_page(request, unitID):

    if unitID != 'none' and UnitModel.objects.filter(id=unitID).exists():
        unit = UnitModel.objects.get(id=unitID)
    elif unitID == 'none':
        unit = None
    elif not unitID:
        return redirect('/404')

    if request.method == 'POST':
        
        if request.POST.get('doctor'):

            doctor = None
            if DoctorModel.objects.filter(id=request.POST.get('doctor')).exists():
                doctor = DoctorModel.objects.get(id=request.POST.get('doctor'))

            if doctor and unit:
                return HttpResponseRedirect(reverse('panel:appointment-timep2', args=(unit.id, doctor.id)))
            elif doctor and not unit:
                return HttpResponseRedirect(reverse('panel:appointment-timep2', args=('none', doctor.id)))            
            else:
                messages.error(request, _('باید حداقل یکی از فیلد ها مقدار داشته باشد.'))
                return redirect('panel:appointment-timep1')

    return render(request, 'panel/online-appointment/time-p1-appointment.html', {
        'doctors': DoctorModel.objects.filter(is_active=True).all(), 
    })


# url: /panel/online-appointment/time/create/<unitID>/<doctorId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_time_create2_page(request, unitID, doctorId):

    if unitID != 'none' and UnitModel.objects.filter(id=unitID).exists():
        unit = UnitModel.objects.get(id=unitID)
    elif unitID == 'none':
        unit = None
    elif not unitID:
        return redirect('/404')

    if doctorId != 'none' and DoctorModel.objects.filter(is_active=True, id=doctorId).exists():
        doctor = DoctorModel.objects.get(is_active=True, id=doctorId)
    elif doctorId == 'none' or not doctorId:
        return redirect('/404')

    if request.method == 'POST':
        form = forms.Time2AppointmentForm(request.POST or None)

        if form.is_valid():
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
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
                    time_from=form.cleaned_data.get('time_from'),
                    time_to=form.cleaned_data.get('time_to'),
                    capacity=form.cleaned_data.get('capacity'),
                    reserved=0,
                    tip=form.cleaned_data.get('tip'),
                )
                # add insurances to queryset
                for item in insurances_obj:
                    time.insurances.add(item)

            form = forms.Time2AppointmentForm()
            messages.success(request, _('زمان نوبت دهی مورد نظر شما با موفقیت اضافه شد.'))
            return redirect('panel:appointment-time')

    else:
        form = forms.Time2AppointmentForm()

    return render(request, 'panel/online-appointment/time-p2-appointment.html', {
        'form': form,
        'insurances': [insurance for insurance in doctor.insurances.all()]
    })


# url: /panel/online-appointment/patient/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_patient_page(request):

    if request.GET.get('paid') == 'yes':
        patients = PatientTurnModel.objects.filter(
            is_paid=True,
            appointment__date__gt=timezone.now()
        ).all()

    elif request.GET.get('paid') == 'no':
        patients = PatientTurnModel.objects.filter(
            is_paid=False,
            appointment__date__gt=timezone.now()
        ).all()

    elif request.GET.get('returned') == 'yes':
        patients = PatientTurnModel.objects.filter(
            is_canceled=True,
            is_returned=True,
            appointment__date__gt=timezone.now()
        ).all()

    elif request.GET.get('returned') == 'no':
        patients = PatientTurnModel.objects.filter(
            is_canceled=True,
            is_returned=False,
            appointment__date__gt=timezone.now()
        ).all()

    else:
        patients = PatientTurnModel.objects.filter(
            appointment__date__gt=timezone.now()
        ).all()

    return render(request, 'panel/online-appointment/patient.html', {
        'patients': patients, 
    })