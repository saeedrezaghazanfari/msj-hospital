from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy
from hospital_auth.models import UserFullNameModel
from hospital_contact.models import NotificationModel
from extentions.utils import safe_string
from . import forms


# url: /panel
@login_required(login_url=reverse_lazy('auth:signin'))
def home_page(request):
    return render(request, 'panel/home.html', {})


# url: /panel/read/notification/<notificationID>/
@login_required(login_url=reverse_lazy('auth:signin'))
def read_notification(request, notificationID):
    if NotificationModel.objects.filter(id=notificationID).exists():
        notif = NotificationModel.objects.get(id=notificationID)
        notif.is_read = True
        notif.save()

        if request.GET.get('route'):
            return redirect(request.GET.get('route'))
        return redirect('website:home')
    return redirect('/404')


# url: /panel/edit-info
@login_required(login_url=reverse_lazy('auth:signin'))
def edit_data(request):

    if request.method == 'POST':
        form = forms.EditInfoForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            if form.cleaned_data.get('email'):
                user.email = form.cleaned_data.get('email')
            if form.cleaned_data.get('profile'):
                user.profile = form.cleaned_data.get('profile')
            user.save()

            if UserFullNameModel.objects.filter(user=user).exists():
                obj = UserFullNameModel.objects.get(user=user)

                if request.POST.get('firstname_fa'):
                    obj.first_name_fa = request.POST.get('firstname_fa')
                    obj.save()
                if request.POST.get('lastname_fa'):
                    obj.last_name_fa = request.POST.get('lastname_fa')
                    obj.save()
                
            else:
                UserFullNameModel.objects.create(
                    user=user,
                    first_name_fa = request.POST.get('firstname_fa') if request.POST.get('firstname_fa') else '',
                    last_name_fa = request.POST.get('lastname_fa') if request.POST.get('lastname_fa') else '',
                    first_name_en='',first_name_ar='', first_name_ru='', last_name_en='', last_name_ar='', last_name_ru=''
                )

            messages.success(request, _('اطلاعات حساب کاربری شما با موفقیت تغییر یافت.'))
            form = forms.EditInfoForm()
            return redirect('panel:editdata')
    
    else:
        form = forms.EditInfoForm(instance=request.user)
        
    return render(request, 'panel/editdata.html', {
        'form': form,
        'firstname_fa': request.user.userfullnamemodel.first_name_fa if UserFullNameModel.objects.filter(user=request.user).exists() else '',
        'firstname_en': request.user.userfullnamemodel.first_name_en if UserFullNameModel.objects.filter(user=request.user).exists() else '',
        'firstname_ar': request.user.userfullnamemodel.first_name_ar if UserFullNameModel.objects.filter(user=request.user).exists() else '',
        'firstname_ru': request.user.userfullnamemodel.first_name_ru if UserFullNameModel.objects.filter(user=request.user).exists() else '',
        'lastname_fa': request.user.userfullnamemodel.last_name_fa if UserFullNameModel.objects.filter(user=request.user).exists() else '',
        'lastname_en': request.user.userfullnamemodel.last_name_en if UserFullNameModel.objects.filter(user=request.user).exists() else '',
        'lastname_ar': request.user.userfullnamemodel.last_name_ar if UserFullNameModel.objects.filter(user=request.user).exists() else '',
        'lastname_ru': request.user.userfullnamemodel.last_name_ru if UserFullNameModel.objects.filter(user=request.user).exists() else '',
    })


# url: /panel/edit-info/fullname/
@login_required(login_url=reverse_lazy('auth:signin'))
def edit_fullname(request):

    if request.method == 'POST':
    
        if UserFullNameModel.objects.filter(user=request.user).exists():
            obj = UserFullNameModel.objects.get(user=request.user)

            if request.POST.get('firstname_en') and safe_string(request, request.POST.get('firstname_en')):
                obj.first_name_en = request.POST.get('firstname_en')
                messages.success(request, _('اطلاعات شما با موفقیت ذخیره شد.'))
                obj.save()
                return redirect('panel:editdata')
            elif request.POST.get('firstname_ar') and safe_string(request, request.POST.get('firstname_ar')):
                obj.first_name_ar = request.POST.get('firstname_ar')
                messages.success(request, _('اطلاعات شما با موفقیت ذخیره شد.'))
                obj.save()
                return redirect('panel:editdata')
            elif request.POST.get('firstname_ru') and safe_string(request, request.POST.get('firstname_ru')):
                obj.first_name_ru = request.POST.get('firstname_ru')
                messages.success(request, _('اطلاعات شما با موفقیت ذخیره شد.'))
                obj.save()
                return redirect('panel:editdata')

            if request.POST.get('lastname_en') and safe_string(request, request.POST.get('lastname_en')):
                obj.last_name_en = request.POST.get('lastname_en')
                messages.success(request, _('اطلاعات شما با موفقیت ذخیره شد.'))
                obj.save()
                return redirect('panel:editdata')
            elif request.POST.get('lastname_ar') and safe_string(request, request.POST.get('lastname_ar')):
                obj.last_name_ar = request.POST.get('lastname_ar')
                messages.success(request, _('اطلاعات شما با موفقیت ذخیره شد.'))
                obj.save()
                return redirect('panel:editdata')
            elif request.POST.get('lastname_ru') and safe_string(request, request.POST.get('lastname_ru')):
                obj.last_name_ru = request.POST.get('lastname_ru')
                messages.success(request, _('اطلاعات شما با موفقیت ذخیره شد.'))
                obj.save()
                return redirect('panel:editdata')

        else:
            messages.info(request, _('باید فیلد های نام و نام خانوادگی فارسی را وارد کنید.'))
            return redirect('panel:editdata')
        
    return redirect('panel:editdata')