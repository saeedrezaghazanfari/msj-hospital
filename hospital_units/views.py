import jdatetime
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from hospital_setting.models import PriceAppointmentModel, InsuranceModel
from hospital_doctor.models import DoctorModel
from .models import (
    AppointmentTimeModel, PatientTurnModel, LimitTurnTimeModel, 
    SubUnitModel, ElectronicPrescriptionModel, ExprimentResultModel, 
    LoginCodePatientModel, 
)
from hospital_auth.models import PatientModel
from . import forms
from extentions.utils import jnum_to_month_name, write_action
# imports for activatings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from hospital_auth.tokens import account_activation_phone_token


# url: /electronic/appointment/
def home_page(request):
    return render(request, 'units/oa-home.html', {})


# url: /electronic/appointment/categories/
def categories_page(request):

    unit_list_index = []
    unit_list = ['doctors']
    times = AppointmentTimeModel.objects.filter(
        # unit__subunit__category='paraclinic',  # show all of units
        date__gt=datetime.now(),
        doctor__is_active=True
    ).iterator()

    for time in times:
        if time.unit and not time.unit.subunit.title in unit_list_index:
            unit_list_index.append(time.unit.subunit.title)
            unit_list.append(time.unit)

    return render(request, 'units/oa-categories.html', {
        'units': unit_list
    })


# url: /electronic/appointment/<unitSlug>/router/
def router_page(request, unitSlug):
    
    if unitSlug == 'doctors' or SubUnitModel.objects.filter(slug=unitSlug, have_2_box=False).exists():
        return redirect(f'/{get_language()}/electronic/appointment/{unitSlug}/')
    elif unitSlug != 'doctors' and SubUnitModel.objects.filter(slug=unitSlug, have_2_box=True).exists():
        return render(request, 'units/oa-router.html', {
            'unitSlug': unitSlug,
        })

    return redirect(f'/{get_language()}/404')


# url: /electronic/appointment/e-prescription/<unitSlug>/phone/
def phone_epresc_page(request, unitSlug):

    if unitSlug == 'doctors' or not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')

    if request.method == 'POST':
        form = forms.PhoneForm(request.POST or None)

        if form.is_valid():
            phone = form.cleaned_data.get('phone')

            code = LoginCodePatientModel.objects.create(
				phone=phone,
			)

            print('code: ', code.code) #TODO delete here

			# + send sms: send code.code #TODO
			# a = requests.get(
			# 	f'https://api.kavenegar.com/v1/{settings.KAVENEGAR_APIKEY}/verify/lookup.json?receptor={phone}&token={code.code}&template=signin'
			# )
			# - sending sms

            uid = urlsafe_base64_encode(force_bytes(code.id)) 
            token = account_activation_phone_token.make_token(code)

            messages.success(request, _('یک پیامک حاوی کلمه ی عبور برای شماره تماس شما ارسال شد.'))
            return redirect(f'/{get_language()}/electronic/appointment/e-prescription/{unitSlug}/enter-sms-code/{uid}/{token}')

    else:
        form = forms.PhoneForm()

    return render(request, 'units/oa-phone.html', {
        'form': form,
    })


# url: /electronic/appointment/e-prescription/<unitSlug>/enter-sms-code/<uidb64>/<token>/
def entercode_pres_page(request, unitSlug, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid, is_use=False, expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')
    
    if unitSlug == 'doctors' or not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')

    if account_activation_phone_token.check_token(code, token):
        
        if request.method == 'POST':
            form = forms.EnterCodePhoneForm(request.POST or None)

            if form.is_valid():
                code_enter = LoginCodePatientModel.objects.filter(
                    code=int(form.cleaned_data.get('code')), 
                    expire_date__gt=timezone.now(),
                    expire_mission__gt=timezone.now(),
                    is_use=False
                ).first()
                
                if code_enter:
                    code_enter.is_use = True
                    code_enter.save()
                    return redirect(f'/{get_language()}/electronic/appointment/e-prescription/{unitSlug}/{uidb64}/{token}/form/') 

                else:
                    messages.error(request, _('کد شما منقضی شده و یا اینکه اعتبار ندارد.'))
                    return redirect(f'/{get_language()}/electronic/appointment/e-prescription/{unitSlug}/enter-sms-code/{uidb64}/{token}') 
        
        else:
            form = forms.EnterCodePhoneForm()

        return render(request, 'units/oa-entercode.html', {
            'form': form
        })
    else:
        return redirect(f'/{get_language()}/404')


# url: /electronic/appointment/e-prescription/<unitSlug>/<uidb64>/<token>/form/
def electronic_pres_page(request, unitSlug, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid, is_use=True, expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')

    if unitSlug == 'doctors' or not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')

    if account_activation_phone_token.check_token(code, token):

        patient_exist = None
        if PatientModel.objects.filter(phone=code.phone).exists():
            patient_exist = PatientModel.objects.get(phone=code.phone)

        if request.method == 'POST':
            form = forms.ElectronicPrescriptionForm(request.POST or None)

            if form.is_valid():

                username = form.cleaned_data.get('username')
                patient = ''

                if PatientModel.objects.filter(username=username).exists():
                    patient = PatientModel.objects.get(username=username)
                    patient.first_name = form.cleaned_data.get('first_name')
                    patient.last_name = form.cleaned_data.get('last_name')
                    patient.phone = code.phone
                    patient.gender = form.cleaned_data.get('gender')
                    patient.age = form.cleaned_data.get('age')
                    patient.created = timezone.now()
                    patient.save()
                else:
                    patient = PatientModel.objects.create(
                        username=form.cleaned_data.get('username'),
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name'),
                        phone=code.phone,
                        gender=form.cleaned_data.get('gender'),
                        age=form.cleaned_data.get('age'),
                    )

                if ElectronicPrescriptionModel.objects.filter(patient=patient, is_send=False).exists():
                    messages.info(request, _('شما یک درخواست بررسی نشده از قبل دارید.'))
                    return redirect(f'/{get_language()}/electronic/appointment/e-prescription/{unitSlug}/{uidb64}/{token}/form/')

                ElectronicPrescriptionModel.objects.create(
                    patient=patient,
                    experiment_code=form.cleaned_data.get('experiment_code'),
                )

                write_action(f'user via {username} nationalCode sent request for e-prescription.', 'ANONYMOUS')
                messages.success(request, _('درخواست شما با موفقیت ارسال شد. بعد از بررسی درخواست شما یک پیامک ارسال خواهد شد. ممنون از صبر و شکیبایی شما.'))
                return redirect(f'/{get_language()}/electronic/appointment/e-prescription/{unitSlug}/{uidb64}/{token}/show-details/')
        
        else:
            form = forms.ElectronicPrescriptionForm(initial={
                'username': patient_exist.username if patient_exist else None,
                'first_name': patient_exist.first_name if patient_exist else None,
                'last_name': patient_exist.last_name if patient_exist else None,
                'gender': patient_exist.gender if patient_exist else None,
                'age': patient_exist.age if patient_exist else None,
            })

        return render(request, 'units/oa-prescription.html', {
            'form': form,
            'have_folder': True if patient_exist else False,
            'uidb64': uidb64,
            'token': token,
            'unitSlug': unitSlug
        })
    return redirect(f'/{get_language()}/404')


# url: /electronic/appointment/e-prescription/<unitSlug>/<uidb64>/<token>/show-details/
def showdetails_pres_page(request, unitSlug, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid, is_use=True, expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')

    if unitSlug == 'doctors' or not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')
    if account_activation_phone_token.check_token(code, token):
        return render(request, 'units/oa-showdetails-pres.html')
    return redirect(f'/{get_language()}/403')


# url: /electronic/appointment/<unitSlug>/
def unit_page(request, unitSlug):
    
    list_medicalcode = []
    list_doctors = []
    subunit = None

    # doctors
    if unitSlug == 'doctors':

        if request.GET.get('type') == 'all' or not request.GET.get('type'):
            times = AppointmentTimeModel.objects.filter(
                unit__isnull=True,
                date__gt=datetime.now(),
                doctor__is_active=True
            ).all()

        elif request.GET.get('type') == 'expert':
            times = AppointmentTimeModel.objects.filter(
                unit__isnull=True,
                date__gt=datetime.now(),
                doctor__is_active=True,
                doctor__degree__title_fa='متخصص'
            ).all()

        elif request.GET.get('type') == 'specialty':
            times = AppointmentTimeModel.objects.filter(
                unit__isnull=True,
                date__gt=datetime.now(),
                doctor__is_active=True,
                doctor__degree__title_fa='فوق تخصص'
            ).all()
        
        elif request.GET.get('type') == 'fellowship':
            times = AppointmentTimeModel.objects.filter(
                unit__isnull=True,
                date__gt=datetime.now(),
                doctor__is_active=True,
                doctor__degree__title_fa='فلوشیپ'
            ).all()

    # no doctors
    elif unitSlug != 'doctors' and SubUnitModel.objects.filter(slug=unitSlug).exists():

        subunit = SubUnitModel.objects.get(slug=unitSlug)

        if request.GET.get('type') == 'all' or not request.GET.get('type'):
            times = AppointmentTimeModel.objects.filter(
                unit__subunit=subunit,
                date__gt=datetime.now(),
                doctor__is_active=True
            ).all()

        elif request.GET.get('type') == 'expert':
            times = AppointmentTimeModel.objects.filter(
                unit__subunit=subunit,
                date__gt=datetime.now(),
                doctor__is_active=True,
                doctor__degree__title_fa='متخصص'
            ).all()

        elif request.GET.get('type') == 'specialty':
            times = AppointmentTimeModel.objects.filter(
                unit__subunit=subunit,
                date__gt=datetime.now(),
                doctor__is_active=True,
                doctor__degree__title_fa='فوق تخصص'
            ).all()

        elif request.GET.get('type') == 'fellowship':
            times = AppointmentTimeModel.objects.filter(
                unit__subunit=subunit,
                date__gt=datetime.now(),
                doctor__is_active=True,
                doctor__degree__title_fa='فلوشیپ'
            ).all()

    else:
        return redirect(f'/{get_language()}/404')

    if times:
        for time in times:
            if not time.doctor.medical_code in list_medicalcode:
                list_medicalcode.append(time.doctor.medical_code)
                list_doctors.append(time.doctor)

    return render(request, 'units/oa-doctors.html', {
        'doctors': list_doctors,
        'header': subunit.title if subunit else _('doctors'),
        'unitSlug': unitSlug,
    })


# url: /electronic/appointment/<unitSlug>/<doctorID>/phone/
def phone_page(request, unitSlug, doctorID):

    if unitSlug != 'doctors' and not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')
    if not doctorID and not DoctorModel.objects.filter(id=doctorID, is_active=True).exists():
        return redirect(f'/{get_language()}/404')
        
    doctor = DoctorModel.objects.get(id=doctorID, is_active=True)

    if request.method == 'POST':
        form = forms.PhoneForm(request.POST or None)

        if form.is_valid():
            phone = form.cleaned_data.get('phone')

            code = LoginCodePatientModel.objects.create(
				phone=phone
			)

            print('code: ', code.code) #TODO delete here

			# + send sms: send code.code #TODO
			# a = requests.get(
			# 	f'https://api.kavenegar.com/v1/{settings.KAVENEGAR_APIKEY}/verify/lookup.json?receptor={phone}&token={code.code}&template=signin'
			# )
			# - sending sms

            uid = urlsafe_base64_encode(force_bytes(code.id)) 
            token = account_activation_phone_token.make_token(code)
            messages.success(request, _('یک پیامک حاوی کلمه ی عبور برای شماره تماس شما ارسال شد.'))
            return redirect(f'/{get_language()}/electronic/appointment/{unitSlug}/enter-sms-code/{doctor.id}/{uid}/{token}')
    
    else:
        form = forms.PhoneForm()

    return render(request, 'units/oa-phone.html', {
        'form': form,
    })


# url: /electronic/appointment/<unitSlug>/enter-sms-code/<doctorID>/<uidb64>/<token>/
def entercode_page(request, unitSlug, doctorID, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid, is_use=False, expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')
    
    if unitSlug != 'doctors' and not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')
    if not doctorID or not DoctorModel.objects.filter(id=doctorID, is_active=True).exists():
        return redirect(f'/{get_language()}/404')

    if account_activation_phone_token.check_token(code, token):
        
        if request.method == 'POST':
            form = forms.EnterCodePhoneForm(request.POST or None)

            if form.is_valid():
                code_enter = LoginCodePatientModel.objects.filter(
                    code=int(form.cleaned_data.get('code')), 
                    expire_date__gt=timezone.now(),
                    expire_mission__gt=timezone.now(),
                    is_use=False
                ).first()
                
                if code_enter:
                    code_enter.is_use = True
                    code_enter.save()
                    return redirect(f'/{get_language()}/electronic/appointment/{unitSlug}/{doctorID}/{uidb64}/{token}/1/calendar/')

                else:
                    messages.error(request, _('کد شما منقضی شده و یا اینکه اعتبار ندارد.'))
                    return redirect(f'/{get_language()}/electronic/appointment/{unitSlug}/enter-sms-code/{doctorID}/{uidb64}/{token}') 
        
        else:
            form = forms.EnterCodePhoneForm()

        return render(request, 'units/oa-entercode.html', {
            'form': form
        })
    else:
        return redirect(f'/{get_language()}/404')


# url: /electronic/appointment/<unitSlug>/<doctorID>/<uidb64>/<token>/<monthNum>/calendar/
def calendar_page(request, unitSlug, doctorID, uidb64, token, monthNum):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid, is_use=True, expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')

    if not monthNum or int(monthNum) <= 0 or int(monthNum) >= 7:
        return redirect(f'/{get_language()}/404')
    if unitSlug != 'doctors' and not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')
    if not doctorID or not DoctorModel.objects.filter(id=doctorID, is_active=True).exists():
        return redirect(f'/{get_language()}/404')

    if account_activation_phone_token.check_token(code, token):
        
        doctor = DoctorModel.objects.get(id=doctorID, is_active=True)
        times = None

        if unitSlug == 'doctors':
            times = AppointmentTimeModel.objects.filter(
                unit__isnull=True,
                doctor=doctor,
                date__gt=timezone.now(),
            ).order_by('date').all()

        elif SubUnitModel.objects.filter(slug=unitSlug).exists():
            times = AppointmentTimeModel.objects.filter(
                unit__subunit__slug=unitSlug,
                doctor=doctor,
                date__gt=timezone.now(),
            ).order_by('date').all()

        limit_time = 6
        if LimitTurnTimeModel.objects.exists():
            limit_obj = LimitTurnTimeModel.objects.first()
            limit_time = limit_obj.hours

        # set limit time for time objects
        for time in times:
            time_str = str(time.date)
            time_list = time_str.split('-')
            time_mined = f'{time_list[0][2]}{time_list[0][3]}-{time_list[1]}-{time_list[2]}'
            time_splited = time.time_from.split(':')

            date_time_obj = datetime.strptime(time_mined, '%y-%m-%d').replace(
                hour=int(time_splited[0]), 
                minute=int(time_splited[1])
            )
            time.is_active = False
            if date_time_obj > datetime.now():
                if (date_time_obj - datetime.now()) > timedelta(hours=limit_time):
                    time.is_active = True


        times_index = jdatetime.date.fromgregorian(day=times[0].date.day, month=times[0].date.month, year=times[0].date.year).month
        this_month = None
        monthNum = int(monthNum)
        times_arr = []

        if not monthNum or monthNum == 1:
            for time in times:
                jalali_date =  jdatetime.date.fromgregorian(day=time.date.day, month=time.date.month, year=time.date.year) 
                
                if jalali_date.month == times_index:
                    times_arr.append(time)
                    this_month = jnum_to_month_name(jalali_date.month)
                elif jalali_date.month > times_index:
                    break


        elif monthNum and monthNum > 1:
            times_index += (monthNum - 1)

            if times_index == 13:
                times_index = 1
            elif times_index == 14:
                times_index = 2

            for time in times:
                jalali_date = jdatetime.date.fromgregorian(day=time.date.day, month=time.date.month, year=time.date.year)

                if jalali_date.month == times_index:
                    times_arr.append(time)
                    this_month = jnum_to_month_name(jalali_date.month)

                elif jalali_date.month > times_index:
                    break

        next = None
        prev = None

        if monthNum and (monthNum + 1) < 7:
            next = monthNum + 1
        elif not monthNum:
            next = 2
        if monthNum and (monthNum - 1) >= 1:
            prev = monthNum - 1 


        #TODO next button is disable when no have any time

        return render(request, 'units/oa-calendar.html', {
            'times': times_arr,
            'doctor': doctor,
            'uidb64': uidb64,
            'token': token,
            'unitSlug': unitSlug,

            'month': this_month,
            'next': next,
            'prev': prev,
        })

    else:
        return redirect(f'/{get_language()}/404')


# url: /electronic/appointment/<unitSlug>/<doctorID>/<appointmentID>/<uidb64>/<token>/info/
def info_page(request, unitSlug, doctorID, appointmentID, uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid, expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')

    if unitSlug != 'doctors' and not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')
    if not doctorID or not DoctorModel.objects.filter(id=doctorID, is_active=True).exists():
        return redirect(f'/{get_language()}/404')
    if not appointmentID or not AppointmentTimeModel.objects.filter(id=appointmentID).exists():
        return redirect(f'/{get_language()}/404')

    if account_activation_phone_token.check_token(code, token):
        # doctor = DoctorModel.objects.get(medical_code=doctorID, is_active=True)
        appointment = AppointmentTimeModel.objects.get(id=appointmentID)

        patient_exist = None
        if PatientModel.objects.filter(phone=code.phone).exists():
            patient_exist = PatientModel.objects.get(phone=code.phone)

        if request.method == 'POST':
            form = forms.PatientForm(request.POST or None)

            if form.is_valid():

                get_insurance = request.POST.get('insurance')
                insurance_user = None
                if get_insurance != 'free' and InsuranceModel.objects.filter(id=get_insurance).exists():
                    insurance_user = InsuranceModel.objects.get(id=get_insurance)

                username = form.cleaned_data.get('username')
                patient = ''

                if PatientModel.objects.filter(username=username).exists():
                    patient = PatientModel.objects.get(username=username)
                    patient.first_name = form.cleaned_data.get('first_name')
                    patient.last_name = form.cleaned_data.get('last_name')
                    patient.phone = code.phone
                    patient.gender = form.cleaned_data.get('gender')
                    patient.age = form.cleaned_data.get('age')
                    patient.created = timezone.now()
                    patient.save()
                else:
                    patient = PatientModel.objects.create(
                        username=form.cleaned_data.get('username'),
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name'),
                        phone=code.phone,
                        gender=form.cleaned_data.get('gender'),
                        age=form.cleaned_data.get('age'),
                    )

                if PatientTurnModel.objects.filter(patient=patient, appointment=appointment, is_paid=False).exists():
                    PatientTurnModel.objects.filter(patient=patient, appointment=appointment, is_paid=False).all().delete()
                    
                turn = PatientTurnModel(
                    patient=patient,
                    appointment=appointment,
                    insurance=insurance_user,
                    prescription_code=form.cleaned_data.get('prescription_code'),
                    experiment_code=form.cleaned_data.get('experiment_code'),
                )

                if insurance_user:
                    if PriceAppointmentModel.objects.filter(insurance=insurance_user, degree=appointment.doctor.degree).exists():
                        price_obj = PriceAppointmentModel.objects.get(insurance=insurance_user, degree=appointment.doctor.degree)
                        turn.price = price_obj.price
                        turn.save()
                else:
                    if PriceAppointmentModel.objects.filter(insurance=None, degree=appointment.doctor.degree).exists():
                        price_obj = PriceAppointmentModel.objects.get(insurance=None, degree=appointment.doctor.degree)
                        turn.price = price_obj.price
                        turn.save()
                    else:
                        return redirect(f'/{get_language()}/404')

                messages.success(request, _('اطلاعات شما با موفقیت ذخیره شد.'))
                return redirect(f'/{get_language()}/electronic/appointment/{unitSlug}/{turn.id}/{uidb64}/{token}/show-details/')
        
        else:
            form = forms.PatientForm(initial={
                'username': patient_exist.username if patient_exist else None,
                'first_name': patient_exist.first_name if patient_exist else None,
                'last_name': patient_exist.last_name if patient_exist else None,
                'gender': patient_exist.gender if patient_exist else None,
                'age': patient_exist.age if patient_exist else None,
            })

        return render(request, 'units/oa-info.html', {
            'form': form,
            'have_folder': True if patient_exist else False,
            'appointment': appointment,
            'insurances': appointment.insurances.all(),
            'uidb64': uidb64,
            'token': token,
            'unitSlug': unitSlug
        })

    else:
        return redirect(f'/{get_language()}/404')


# url: /electronic/appointment/<unitSlug>/<patientTurnId>/<uidb64>/<token>/show-details/
def showdetails_page(request, unitSlug, patientTurnId, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid, expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')

    if unitSlug != 'doctors' and not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')
    if not patientTurnId or not PatientTurnModel.objects.filter(id=patientTurnId).exists():
        return redirect(f'/{get_language()}/404')

    if account_activation_phone_token.check_token(code, token):
        patient_turn = PatientTurnModel.objects.get(id=patientTurnId)

        return render(request, 'units/oa-showdetails.html', {
            'turn': patient_turn,
            'uidb64': uidb64,
            'token': token,
            'unitSlug': unitSlug
        })
    else:
        return redirect(f'/{get_language()}/404')


# url: /electronic/appointment/<unitSlug>/<patientTurnId>/<uidb64>/<token>/trust/
def trust_page(request, unitSlug, patientTurnId, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid, expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')

    if unitSlug != 'doctors' and not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')
    if not patientTurnId or not PatientTurnModel.objects.filter(id=patientTurnId).exists():
        return redirect(f'/{get_language()}/404')

    if account_activation_phone_token.check_token(code, token):
        
        patient_turn = PatientTurnModel.objects.get(id=patientTurnId)
        limit_time = LimitTurnTimeModel.objects.first()

        if request.method == 'POST':
            form = forms.CheckRulesForm(request.POST or None)

            if form.is_valid():

                #TODO send user to payment site
                # price: patient_turn.price
                print('you are going to ...')
                # redirected to payment

        else:
            form = forms.CheckRulesForm()

        return render(request, 'units/oa-trust.html', {
            'form': form,
            'turn': patient_turn,
            'limit_time': limit_time.rules if limit_time else None,
            'tips': patient_turn.appointment.tip.tips,
            'uidb64': uidb64,
            'token': token,
        })
    else:
        return redirect(f'/{get_language()}/404')


# url: /electronic/appointment/<unitSlug>/<patientTurnId>/<uidb64>/<token>/end/
def end_page(request, unitSlug, patientTurnId, uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid, expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')

    if unitSlug != 'doctors' and not SubUnitModel.objects.filter(slug=unitSlug).exists():
        return redirect(f'/{get_language()}/404')
    if not patientTurnId or not PatientTurnModel.objects.filter(id=patientTurnId).exists():
        return redirect(f'/{get_language()}/404')

    if account_activation_phone_token.check_token(code, token):
        
        patient_turn = PatientTurnModel.objects.get(id=patientTurnId)

        # TODO these are lines
        # patient_turn.is_paid = True
        # patient_turn.appointment.reserved += 1
        # patient_turn.appointment.save()
        # patient_turn.turn = patient_turn.appointment.reserved
        # patient_turn.save()

        # OnlinePaymentModel.objects.create(
        #     payer=patient_turn,
        #     price=patient_turn.price,
        #     is_success=True,
        #     code=None #TODO
        # )

        #TODO create write action for this patinet

        #TODO SMS to user for code peygiri

        return render(request, 'units/oa-end.html', {
            'turn': patient_turn,
        })
    else:
        return redirect(f'/{get_language()}/404')


# url: /electronic/appointment/turn/
def followturn_page(request):

    turn = None
    msg = None

    if request.method == 'POST':
        form = forms.FollowUpTurnForm(request.POST or None)

        if form.is_valid():

            if not PatientTurnModel.objects.filter(code=form.cleaned_data.get('code'), patient__phone=form.cleaned_data.get('phone')).exists():
                return redirect(f'/{get_language()}/404')
            turn = PatientTurnModel.objects.get(code=form.cleaned_data.get('code'), patient__phone=form.cleaned_data.get('phone'))
            
            if turn.appointment.status == 'invac':
                msg = _('پزشک مورد نظر به مرخصی رفته است و نوبت شما به تعویق افتاده است.')

    else:
        form = forms.FollowUpTurnForm()

    return render(request, 'units/oa-followup-turn.html', {
        'form': form,
        'turn': turn,
        'msg': msg,
    })


# url: /electronic/appointment/result/
def followresult_page(request):

    result = None

    if request.method == 'POST':
        form = forms.FollowUpResultForm(request.POST or None)

        if form.is_valid():
            if not ExprimentResultModel.objects.filter(code=form.cleaned_data.get('code'), patient__phone=form.cleaned_data.get('phone')).exists():
                return redirect(f'/{get_language()}/404')
            else:
                result = ExprimentResultModel.objects.get(code=form.cleaned_data.get('code'), patient__phone=form.cleaned_data.get('phone'))
                # TODO send request to FACS

    else:
        form = forms.FollowUpResultForm()

    return render(request, 'units/oa-followup-result.html', {
        'form': form,
        'result': result
    })


# edit ExprimentResultModel  ---   fields: patient_id, patinet_phone