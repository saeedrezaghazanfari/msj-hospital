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
                obj.first_name_fa = form.cleaned_data.get('firstname')
                obj.last_name_fa = form.cleaned_data.get('lastname')
                obj.first_name_en = form.cleaned_data.get('firstname')
                obj.last_name_en = form.cleaned_data.get('lastname')
                obj.first_name_ar = form.cleaned_data.get('firstname')
                obj.last_name_ar = form.cleaned_data.get('lastname')
                obj.first_name_ru = form.cleaned_data.get('firstname')
                obj.last_name_ru = form.cleaned_data.get('lastname')
                obj.save()
            else:
                UserFullNameModel.objects.create(
                    user=user,
                    first_name_fa = form.cleaned_data.get('firstname'),
                    last_name_fa = form.cleaned_data.get('lastname'),
                    first_name_en = form.cleaned_data.get('firstname'),
                    last_name_en = form.cleaned_data.get('lastname'),
                    first_name_ar = form.cleaned_data.get('firstname'),
                    last_name_ar = form.cleaned_data.get('lastname'),
                    first_name_ru = form.cleaned_data.get('firstname'),
                    last_name_ru = form.cleaned_data.get('lastname'),	
                )

            messages.success(request, _('اطلاعات حساب کاربری شما با موفقیت تغییر یافت.'))
            form = forms.EditInfoForm()
            return redirect('panel:home')

    else:
        form = forms.EditInfoForm(instance=request.user, initial={
            'firstname': request.user.firstname,
            'lastname': request.user.lastname,
        })
        
    return render(request, 'panel/editdata.html', {
        'form': form
    })

