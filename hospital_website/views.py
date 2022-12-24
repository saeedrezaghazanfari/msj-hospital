from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from hospital_setting.models import PriceAppointmentModel
from hospital_blog.models import BlogModel
from hospital_doctor.models import DoctorModel
from hospital_units.models import UnitModel, AppointmentTimeModel, PatientTurnModel, LimitTurnTimeModel
from hospital_auth.models import PatientModel
from . import forms
from .models import LoginCodePatientModel
# imports for activatings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from hospital_auth.tokens import account_activation_phone_token


# url: /
def home_page(request):
    return render(request, 'web/home.html', {})


# url: /electronic/appointment/
def eoa_home_page(request):
    return render(request, 'web/electronic-services/oa-home.html', {})


# url: /electronic/appointment/categories/
def eoa_categories_page(request):
    return render(request, 'web/electronic-services/oa-categories.html', {})


# url: /electronic/appointment/categories/doctors/
def eoa_doctors_page(request):
    doctors = AppointmentTimeModel.objects.filter(
                unit__isnull=True,
                date__gt=datetime.now(),
                doctor__is_active=True
            ).values(
                'doctor__medical_code', 
                'doctor__user__first_name', 
                'doctor__user__last_name', 
                'doctor__skill_title__title', 
                'doctor__degree__title', 
            ).iterator()

    list_medicalcode = []
    list_doctors = []

    for doctor in doctors:
        if not doctor['doctor__medical_code'] in list_medicalcode:
            list_medicalcode.append(doctor['doctor__medical_code'])
            list_doctors.append(doctor)

    return render(request, 'web/electronic-services/oa-doctors.html', {
        'doctors': list_doctors,
    })


# url: /electronic/appointment/<int:medicalCode>/phone/
def eoa_phone_page(request, medicalCode):

    if not medicalCode and not DoctorModel.objects.filter(medical_code=medicalCode, is_active=True).exists():
        return redirect('/404')
        
    doctor = DoctorModel.objects.get(medical_code=medicalCode, is_active=True)
    get_phone = forms.PhoneForm(request.POST or None)
    context = {
        'form': get_phone,
    }
    if request.method == 'POST':
        if get_phone.is_valid():

            phone = get_phone.cleaned_data.get('phone')

            code = LoginCodePatientModel.objects.create(
				phone=phone,
                usage='appointment'
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
            return redirect(f'/{get_language()}/electronic/appointment/enter-sms-code/{doctor.medical_code}/{uid}/{token}')

    return render(request, 'web/electronic-services/oa-phone.html', context)


# url: /electronic/appointment/enter-sms-code/<medicalCode>/<uidb64>/<token>
def eoa_entercode_page(request, medicalCode, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect('/404')
    
    if not medicalCode or not DoctorModel.objects.filter(medical_code=int(medicalCode), is_active=True).exists():
        return redirect('/404')

    if account_activation_phone_token.check_token(code, token):
        form = forms.EnterCodePhoneForm(request.POST or None)
        context = {'form': form}

        if request.method == 'POST':
            if form.is_valid():

                code_enter = LoginCodePatientModel.objects.filter(
                    code=int(form.cleaned_data.get('code')), 
                    expire_date__gt=timezone.now(), 
                    usage='appointment', 
                    is_use=False
                ).first()
                
                if code_enter:
                    code_enter.is_use = True
                    code_enter.save()

                    context['form'] = forms.EnterCodePhoneForm()
                    return redirect(f'/electronic/appointment/{medicalCode}/{uidb64}/{token}/calendar/') 

                else:
                    messages.error(request, _('کد شما منقضی شده و یا اینکه اعتبار ندارد.'))
                    return redirect(f'/electronic/appointment/enter-sms-code/{medicalCode}/{uidb64}/{token}') 

        return render(request, 'web/electronic-services/oa-entercode.html', context)
    else:
        return redirect('/404')


# url: /electronic/appointment/<medicalCode>/<uidb64>/<token>/calendar/
def eoa_calendar_page(request, medicalCode, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect('/404')

    if not medicalCode or not DoctorModel.objects.filter(medical_code=int(medicalCode), is_active=True).exists():
        return redirect('/404')

    if account_activation_phone_token.check_token(code, token):
        
        doctor = DoctorModel.objects.get(medical_code=medicalCode, is_active=True)
        times = AppointmentTimeModel.objects.filter(
            doctor=doctor,#TODO serach for skill - degree
            date__gt=timezone.now(),
        ).iterator()

        # for time in times:
        #     if time.date < timedelta(hours=24): ٫٫٫٫٫٫٫٫٫٫٫٫٫٫٫٫٫٫

        return render(request, 'web/electronic-services/oa-calendar.html', {
            'times': times,
            'doctor': doctor,
            'uidb64': uidb64,
            'token': token,
        })

    else:
        return redirect('/404')


# url: /electronic/appointment/<medicalCode>/<appointmentID>/<uidb64>/<token>/info/
def eoa_info_page(request, medicalCode, appointmentID, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect('/404')

    if not medicalCode or not DoctorModel.objects.filter(medical_code=int(medicalCode), is_active=True).exists():
        return redirect('/404')
    if not appointmentID or not AppointmentTimeModel.objects.filter(id=int(appointmentID)).exists():
        return redirect('/404')

    if account_activation_phone_token.check_token(code, token):
        
        form = forms.PatientForm(request.POST or None)
        context = {
            'form': form
        }

        if request.method == 'POST':
            if form.is_valid():

                username = form.cleaned_data.get('username')
                appointment = AppointmentTimeModel.objects.get(id=int(appointmentID))
                patient = ''

                if PatientModel.objects.filter(username=username).exists():
                    patient = PatientModel.objects.get(username=username)
                    patient.first_name = form.cleaned_data.get('first_name')
                    patient.last_name = form.cleaned_data.get('last_name')
                    patient.phone = form.cleaned_data.get('phone')
                    patient.gender = form.cleaned_data.get('gender')
                    patient.age = form.cleaned_data.get('age')
                    patient.created = timezone.now()
                    patient.save()
                else:
                    patient = PatientModel.objects.create(
                        username=form.cleaned_data.get('username'),
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name'),
                        phone=form.cleaned_data.get('phone'),
                        gender=form.cleaned_data.get('gender'),
                        age=form.cleaned_data.get('age'),
                    )

                insurance = None
                if form.cleaned_data.get('insurance'):
                    insurance = form.cleaned_data.get('insurance')

                turn = PatientTurnModel(
                    patient=patient,
                    appointment=appointment,
                    insurance__title=insurance,
                    prescription_code=form.cleaned_data.get('prescription_code'),
                    experiment_code=form.cleaned_data.get('experiment_code'),
                )

                doctor = DoctorModel.objects.get(medicalCode, is_active=True)

                # if doctor have contract to this patient insurance: 
                if doctor.doctorinsurancemodel_set.filter(insurance_hospital__title=insurance).exists():
                    price_appointment = PriceAppointmentModel.objects.filter(
                        insurance__title=insurance,
                        degree=doctor.degree.title,
                    ).first()

                    turn.price = price_appointment.price_insurance
                    # turn.save()
                else:
                    price_appointment = PriceAppointmentModel.objects.filter(
                        degree=doctor.degree.title,
                    ).first()

                    turn.price = price_appointment.price_free
                    # turn.save()

        return render(request, 'web/electronic-services/oa-info.html', context)

    else:
        return redirect('/404')
