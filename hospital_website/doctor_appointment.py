from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from hospital_setting.models import PriceAppointmentModel, InsuranceModel
from hospital_doctor.models import DoctorModel
from hospital_units.models import AppointmentTimeModel, PatientTurnModel, LimitTurnTimeModel, OnlinePaymentModel
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
            return redirect(f'/{get_language()}/electronic/appointment/enter-sms-code/{doctor.medical_code}/{uid}/{token}')
    
    else:
        form = forms.PhoneForm()

    return render(request, 'web/electronic-services/oa-phone.html', {
        'form': form,
    })


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
        
        if request.method == 'POST':
            form = forms.EnterCodePhoneForm(request.POST or None)

            if form.is_valid():
                code_enter = LoginCodePatientModel.objects.filter(
                    code=int(form.cleaned_data.get('code')), 
                    expire_date__gt=timezone.now(),
                    is_use=False
                ).first()
                
                if code_enter:
                    code_enter.is_use = True
                    code_enter.save()

                    form = forms.EnterCodePhoneForm()
                    return redirect(f'/electronic/appointment/{medicalCode}/{uidb64}/{token}/calendar/') 

                else:
                    messages.error(request, _('کد شما منقضی شده و یا اینکه اعتبار ندارد.'))
                    return redirect(f'/electronic/appointment/enter-sms-code/{medicalCode}/{uidb64}/{token}') 
        
        else:
            form = forms.EnterCodePhoneForm()

        return render(request, 'web/electronic-services/oa-entercode.html', {
            'form': form
        })
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
        ).order_by('-date').all()

        limit_time = 24
        if LimitTurnTimeModel.objects.exists():
            limit_obj = LimitTurnTimeModel.objects.first()
            limit_time = limit_obj.hours

        # set limit time for time objects
        for time in times:
            time_str = str(time.date)
            time_list = time_str.split('-')
            time_mined = f'{time_list[0][2]}{time_list[0][3]}-{time_list[1]}-{time_list[2]}'
            date_time_obj = datetime.strptime(time_mined, '%y-%m-%d')

            time.is_active = False
            if date_time_obj > datetime.now():
                if (date_time_obj - datetime.now()) > timedelta(hours=limit_time):
                    time.is_active = True

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
        # doctor = DoctorModel.objects.get(medical_code=medicalCode, is_active=True)
        appointment = AppointmentTimeModel.objects.get(id=int(appointmentID))

        patient_exist = None
        if PatientModel.objects.filter(phone=code.phone).exists():
            patient_exist = PatientModel.objects.get(phone=code.phone)

        if request.method == 'POST':
            form = forms.PatientForm(request.POST or None)

            if form.is_valid():

                get_insurance = request.POST.get('insurance')
                insurance_user = None
                if get_insurance != 'free' and InsuranceModel.objects.filter(title=get_insurance).exists():
                    insurance_user = InsuranceModel.objects.get(title=get_insurance)

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

                form = forms.PatientForm()
                messages.success(request, _('اطلاعات شما با موفقیت ذخیره شد.'))
                return redirect(f'/electronic/appointment/{turn.id}/{uidb64}/{token}/show-details/')
        
        else:
            form = forms.PatientForm(initial={
                'username': patient_exist.username if patient_exist else None,
                'first_name': patient_exist.first_name if patient_exist else None,
                'last_name': patient_exist.last_name if patient_exist else None,
                'gender': patient_exist.gender if patient_exist else None,
                'age': patient_exist.age if patient_exist else None,
            })

        return render(request, 'web/electronic-services/oa-info.html', {
            'form': form,
            'have_folder': True if patient_exist else False,
            'appointment': appointment,
            'insurances': appointment.insurances.all(),
            'uidb64': uidb64,
            'token': token,
        })

    else:
        return redirect('/404')


# url: /electronic/appointment/<patientTurnId>/<uidb64>/<token>/show-details/
def eoa_showdetails_page(request, patientTurnId, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect('/404')

    if not patientTurnId or not PatientTurnModel.objects.filter(id=patientTurnId).exists():
        return redirect('/404')

    if account_activation_phone_token.check_token(code, token):
        patient_turn = PatientTurnModel.objects.get(id=patientTurnId)

        return render(request, 'web/electronic-services/oa-showdetails.html', {
            'turn': patient_turn,
            'uidb64': uidb64,
            'token': token,
        })
    else:
        return redirect('/404')


# url: /electronic/appointment/<patientTurnId>/<uidb64>/<token>/trust/
def eoa_trust_page(request, patientTurnId, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect('/404')

    if not patientTurnId or not PatientTurnModel.objects.filter(id=patientTurnId).exists():
        return redirect('/404')

    if account_activation_phone_token.check_token(code, token):
        
        patient_turn = PatientTurnModel.objects.get(id=patientTurnId)
        limit_time = LimitTurnTimeModel.objects.first()

        if request.method == 'POST':
            form = forms.CheckRulesForm(request.POST or None)

            if form.is_valid():

                #TODO send user to payment site
                # price: patient_turn.price
                print('you are going to ...')
                form = forms.CheckRulesForm()

        else:
            form = forms.CheckRulesForm()

        return render(request, 'web/electronic-services/oa-trust.html', {
            'form': form,
            'turn': patient_turn,
            'limit_time': limit_time.rules if limit_time else None,
            'tips': patient_turn.appointment.tip.tips,
            'uidb64': uidb64,
            'token': token,
        })
    else:
        return redirect('/404')


# url: /electronic/appointment/<patientTurnId>/<uidb64>/<token>/end/
def eoa_end_page(request, patientTurnId, uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = LoginCodePatientModel.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, LoginCodePatientModel.DoesNotExist):
        code = None
        return redirect('/404')

    if not patientTurnId or not PatientTurnModel.objects.filter(id=patientTurnId).exists():
        return redirect('/404')

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

        #TODO SMS to user for code peygiri

        return render(request, 'web/electronic-services/oa-end.html', {
            'turn': patient_turn,
        })
    else:
        return redirect('/404')