from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib import messages
from extentions.utils import write_action
from .models import IPDModel, IPDCodeModel 
from . import forms
# imports for activatings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from hospital_auth.tokens import account_activation_phone_token


# url: /ipd/phone/
def enter_phone_page(request):

    if request.method == 'POST':
        form = forms.PhoneForm(request.POST or None)

        if form.is_valid():
            phone = form.cleaned_data.get('phone')

            code = IPDCodeModel.objects.create(
				phone=phone
			)

            print('IPD code: ', code.code) #TODO delete here

			# + send sms: send code.code #TODO
			# a = requests.get(
			# 	f'https://api.kavenegar.com/v1/{settings.KAVENEGAR_APIKEY}/verify/lookup.json?receptor={phone}&token={code.code}&template=signin'
			# )
			# - sending sms

            uid = urlsafe_base64_encode(force_bytes(code.id)) 
            token = account_activation_phone_token.make_token(code)

            messages.success(request, _('یک پیامک حاوی کلمه ی عبور برای شماره تماس شما ارسال شد.'))
            return redirect(f'/{get_language()}/ipd/enter-sms-code/{uid}/{token}/')
    
    else:
        form = forms.PhoneForm()

    return render(request, 'ipd/phone.html', {
        'form': form,
    })


# url: /ipd/enter-sms-code/<uidb64>/<token>/
def enter_smscode_page(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = IPDCodeModel.objects.get(id=uid, is_use=False, expire_date__gt=timezone.now(), expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, IPDCodeModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')

    if account_activation_phone_token.check_token(code, token):
        
        if request.method == 'POST':
            form = forms.EnterCodePhoneForm(request.POST or None)

            if form.is_valid():
                code_enter = IPDCodeModel.objects.filter(
                    code=int(form.cleaned_data.get('code')), 
                    expire_date__gt=timezone.now(),
                    expire_mission__gt=timezone.now(),
                    is_use=False
                ).first()
                
                if code_enter:
                    code_enter.is_use = True
                    code_enter.save()
                    return redirect(f'/{get_language()}/ipd/register/{uidb64}/{token}/')

                else:
                    messages.error(request, _('کد شما منقضی شده و یا اینکه اعتبار ندارد.'))
                    return redirect(f'/{get_language()}/ipd/enter-sms-code/{uid}/{token}/')
        
        else:
            form = forms.EnterCodePhoneForm()

        return render(request, 'ipd/sms-code.html', {
            'form': form
        })
    else:
        return redirect(f'/{get_language()}/404')


# url: /ipd/register/<uidb64>/<token>/
def register_page(request, uidb64, token):
    """
        this page must be fill in 30 minutes
    """

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        code = IPDCodeModel.objects.get(id=uid, is_use=True, expire_mission__gt=timezone.now())
    except(TypeError, ValueError, OverflowError, IPDCodeModel.DoesNotExist):
        code = None
        return redirect(f'/{get_language()}/404')

    if account_activation_phone_token.check_token(code, token):
        
        if request.method == 'POST':
            form = forms.IPDForm(request.POST, request.FILES or None)

            country = request.POST.get('country')
            state = request.POST.get('state')
            city = request.POST.get('city')

            if not country or not state or not city:
                messages.error(request, _('باید مقادیر کشور استان و شهر را وارد کنید.'))
                return redirect('auth:ipd-register')

            if form.is_valid():

                new_ipd = form.save(commit=False)
                
                if IPDModel.objects.filter(username=new_ipd.username, is_answered=False).exists():
                    messages.error(request, _('شما قبلا یک فرم ارسال کرده اید. در صورتی که به آن فرم پاسخ داده شده باشد میتوانید فرم جدید ارسال کنید.'))
                    return redirect('website:home')

                new_ipd.phone = code.phone
                new_ipd.country = country
                new_ipd.state = state
                new_ipd.city = city

                new_ipd.save()
                write_action(f'user via {new_ipd.username} nationalCode/passport sent ipd form.', 'ANONYMOUS')

                # TODO send sms to new_ipd.phone

                messages.success(request, _('فرم شما با موفقیت ارسال شد. تیم پزشکی ما در اسرع وقت درخواست شما را بررسی خواهد کرد.'))
                return redirect('website:home')

        else:
            form = forms.IPDForm()

        return render(request, 'ipd/register.html', {
            'form': form
        })
    
    else:
        return redirect(f'/{get_language()}/404')


# url: /ipd/login/
def login_page(request):

    if request.method == 'POST':
        form = forms.LoginForm(request.POST or None)

        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            code = form.cleaned_data.get('code')

            ipd_obj = get_object_or_404(IPDModel, code=code, phone=phone, is_answered=True)
            return redirect(f'/{get_language()}/ipd/info/{ipd_obj.id}/')
    
    else:
        form = forms.LoginForm()

    return render(request, 'ipd/login.html', {
        'form': form,
    })


# url: /ipd/info/<ipdId>/
def info_page(request, ipdId):
    
    ipd_obj = get_object_or_404(IPDModel, id=ipdId, is_answered=True)
    
    return render(request, 'ipd/info.html', {
        'ipd': ipd_obj,
    })
