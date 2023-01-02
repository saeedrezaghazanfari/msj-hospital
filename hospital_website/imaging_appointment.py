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


# url: /electronic/appointment/categories/imaging/
def eoa_imaging_page(request):

    return render(request, 'web/electronic-services/imaging/oa-home.html', {})

