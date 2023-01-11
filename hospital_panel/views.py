from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy
from hospital_auth.models import UserFullNameModel
from . import forms


# url: /panel
@login_required(login_url=reverse_lazy('auth:signin'))
def home_page(request):
    return render(request, 'panel/home.html', {})


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
                if request.POST.get('lastname_fa'):
                    obj.last_name_fa = request.POST.get('lastname_fa')
                if request.POST.get('firstname_en'):
                    obj.first_name_en = request.POST.get('firstname_en')
                if request.POST.get('lastname_en'):
                    obj.last_name_en = request.POST.get('lastname_en')
                if request.POST.get('firstname_ar'):
                    obj.first_name_ar = request.POST.get('firstname_ar')
                if request.POST.get('lastname_ar'):
                    obj.last_name_ar = request.POST.get('lastname_ar')
                if request.POST.get('firstname_ru'):
                    obj.first_name_ru = request.POST.get('firstname_ru')
                if request.POST.get('lastname_ru'):
                    obj.last_name_ru = request.POST.get('lastname_ru')
                
                obj.save()

            else:
                UserFullNameModel.objects.create(
                    user=user,
                    first_name_fa = request.POST.get('firstname_fa') if request.POST.get('firstname_fa') else '',
                    last_name_fa = request.POST.get('lastname_fa') if request.POST.get('lastname_fa') else '',
                    first_name_en = request.POST.get('firstname_en') if request.POST.get('firstname_en') else '',
                    last_name_en = request.POST.get('lastname_en') if request.POST.get('lastname_en') else '',
                    first_name_ar = request.POST.get('firstname_ar') if request.POST.get('firstname_ar') else '',
                    last_name_ar = request.POST.get('lastname_ar') if request.POST.get('lastname_ar') else '',
                    first_name_ru = request.POST.get('firstname_ru') if request.POST.get('firstname_ru') else '',
                    last_name_ru = request.POST.get('lastname_ru') if request.POST.get('lastname_ru') else '',	
                )

            messages.success(request, _('اطلاعات حساب کاربری شما با موفقیت تغییر یافت.'))
            form = forms.EditInfoForm()
            return redirect('panel:home')

    else:
        form = forms.EditInfoForm(instance=request.user)
        
    return render(request, 'panel/editdata.html', {
        'form': form,
        'firstname_fa': request.user.userfullnamemodel.first_name_fa,
        'firstname_en': request.user.userfullnamemodel.first_name_en,
        'firstname_ar': request.user.userfullnamemodel.first_name_ar,
        'firstname_ru': request.user.userfullnamemodel.first_name_ru,
        'lastname_fa': request.user.userfullnamemodel.last_name_fa,
        'lastname_en': request.user.userfullnamemodel.last_name_en,
        'lastname_ar': request.user.userfullnamemodel.last_name_ar,
        'lastname_ru': request.user.userfullnamemodel.last_name_ru,
    })

