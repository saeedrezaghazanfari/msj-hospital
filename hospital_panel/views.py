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


# url: /edit-info
@login_required(login_url=reverse_lazy('auth:signin'))
def edit_data(request):
    form = forms.EditInfoForm(request.POST, request.FILES or None, initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    })
    context = {
        'form': form,
    }

    if request.method == 'POST':
        if form.is_valid():
            

            messages.success(request, _('اطلاعات حساب کاربری شما با موفقیت تغییر یافت.'))
            return redirect('')

    return render(request, 'panel/editdata.html', context)


# url: /panel/doctor
@login_required(login_url=reverse_lazy('auth:signin'))
def doctor_page(request):
    return render(request, 'panel/doctor/home.html', {})


# url: /panel/blog
@login_required(login_url=reverse_lazy('auth:signin'))
def blog_page(request):
    return render(request, 'panel/blog/home.html', {})


# url: /panel/news
@login_required(login_url=reverse_lazy('auth:signin'))
def news_page(request):
    return render(request, 'panel/news/home.html', {})


# url: /panel/notes
@login_required(login_url=reverse_lazy('auth:signin'))
def notes_page(request):
    return render(request, 'panel/notes/home.html', {})


# url: /panel/experiment
@login_required(login_url=reverse_lazy('auth:signin'))
def experiment_page(request):
    return render(request, 'panel/experiment/home.html', {})

