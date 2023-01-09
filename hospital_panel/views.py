from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy
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
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            if form.cleaned_data.get('email'):
                user.email = form.cleaned_data.get('email')
            if form.cleaned_data.get('profile'):
                user.profile = form.cleaned_data.get('profile')
            user.save()

            messages.success(request, _('اطلاعات حساب کاربری شما با موفقیت تغییر یافت.'))
            form = forms.EditInfoForm()
            return redirect('panel:home')

    else:
        form = forms.EditInfoForm(instance=request.user)
        
    return render(request, 'panel/editdata.html', {
        'form': form
    })

