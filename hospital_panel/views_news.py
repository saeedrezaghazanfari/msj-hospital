from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .decorators import news_required
from . import forms


# url: /panel/news
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required
def news_page(request):
    return render(request, 'panel/news/home.html', {})