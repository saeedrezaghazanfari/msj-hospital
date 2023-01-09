import calendar
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from hospital_blog.models import BlogModel
from .decorators import blog_required
from . import forms


# url: /panel/blog
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url='/403')
def blog_page(request):
    blogs = BlogModel.objects.filter(
        is_publish=True,
        is_activate=True
    ).all()

    return render(request, 'blog/list.html', {
        'blogs': blogs
    })