from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from hospital_auth.models import User
# from .forms import EditInfoForm


# url: /panel
@login_required(login_url=reverse_lazy('auth:signin'))
def home_page(request):
    return render(request, 'panel/home.html', {})


# url: /edit-info
@login_required(login_url=reverse_lazy('auth:signin'))
def edit_data(request):
    return render(request, 'panel/editdata.html', {})


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

