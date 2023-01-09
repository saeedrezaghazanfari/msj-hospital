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


# url: /panel/blog/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url='/403')
def blog_page(request):
    blogs = BlogModel.objects.filter(
        writer=request.user,
    ).all()

    return render(request, 'panel/blog/home.html', {
        'blogs': blogs
    })


# url: /panel/blog/create/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url='/403')
def blog_create_page(request):

    if request.method == 'POST':
        form = forms.BlogForm(request.POST, request.FILES or None)

        if form.is_valid():

            is_activate = False
            if request.user.is_blog_manager:
                is_activate = True
            
            BlogModel.objects.create(
                writer=request.user,
                is_activate=is_activate,
            )

            messages.success(request, _('بلاگ با موفقیت ایجاد شد.'))
            return redirect('panel:blog-list')

    else:
        form = forms.BlogForm()

    return render(request, 'panel/blog/create.html', {
        'form': form
    })


# url: /panel/blog/edit/<blogSlug>/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url='/403')
def blog_edit_page(request):
    blogs = BlogModel.objects.filter(
        is_publish=True,
        is_activate=True
    ).all()

    return render(request, 'panel/blog/edit.html', {
        'blogs': blogs
    })