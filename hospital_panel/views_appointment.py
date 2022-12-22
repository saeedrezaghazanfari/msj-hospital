from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from hospital_units.models import LimitTurnTimeModel
from hospital_setting.models import PriceAppointmentModel
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
    
    limit_time = LimitTurnTimeModel.objects.last()
    return render(request, 'panel/online-appointment/limittime.html', {
        'limit_time': limit_time
    })


# url: /panel/online-appointment/insurances/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_insurances_page(request):
    return render(request, 'panel/online-appointment/insurances.html')


# url: /panel/online-appointment/tips/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_tips_page(request):
    return render(request, 'panel/online-appointment/tips.html')


# url: /panel/online-appointment/doctor/list/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_doctorlist_page(request):
    return render(request, 'panel/online-appointment/doctor-list.html')


# url: /panel/online-appointment/price/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required
def oa_price_page(request):

    create_form = forms.CreatePriceAppointmentForm(request.POST or None)
    prices = PriceAppointmentModel.objects.all()
    context = {
        'prices': prices,
        'form': create_form,
    }

    if request.method == 'POST':
        if create_form.is_valid():
            create_form.save()
            context['form'] = forms.CreatePriceAppointmentForm()

            messages.success(request, _('تعرفه ی مورد نظر شما با موفقیت اضافه شد.'))
            return redirect('panel:appointment-price')

    return render(request, 'panel/online-appointment/price-appointment.html', context)