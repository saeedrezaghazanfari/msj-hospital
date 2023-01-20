from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from hospital_blog.models import BlogModel
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from .decorators import blog_required
from hospital_blog.models import TagModel, CategoryModel, BlogGalleryModel
from hospital_setting.models import NewsLetterEmailsModel
from . import forms


# url: /panel/blog/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url='/403')
def blog_page(request):
    unpub_blogs = BlogModel.objects.filter(
        writer=request.user,
        is_publish=False,
    ).all()

    blogs = BlogModel.objects.filter(
        writer=request.user,
    ).all()

    return render(request, 'panel/blog/home.html', {
        'unpub_blogs': unpub_blogs,
        'blogs': blogs,
    })


# url: /panel/blog/create/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url='/403')
def blog_create_page(request):

    if request.method == 'POST':
        form = forms.BlogForm(request.POST, request.FILES or None)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.writer = request.user
            blog.save()

            if blog.is_publish and not blog.is_emailed:

                #TODO send shared email 

                emails = NewsLetterEmailsModel.objects.all().values('email')

                mail_subject = _('بیمارستان موسی ابن جعفر - پست جدید')
                messagee = render_to_string('panel/email-templates/new-blog.html', {
                    'blog': blog,
                    'domain': get_current_site(request).domain,
                })
                
                msg_EMAIL = EmailMessage(
                    mail_subject, messagee, from_email=settings.EMAIL_HOST_USER, to=emails
                )
                msg_EMAIL.content_subtype = "html"
                # msg_EMAIL.send()

                blog.is_emailed = True
                blog.save()

            messages.success(request, _('بلاگ با موفقیت ویرایش شد.'))
            return redirect('panel:blog-list')

            messages.success(request, _('بلاگ با موفقیت ذخیره شد.'))
            return redirect('panel:blog-list')

    else:
        form = forms.BlogForm()

    return render(request, 'panel/blog/create.html', {
        'form': form
    })


# url: /panel/blog/edit/<blogSlug>/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url='/403')
def blog_edit_page(request, blogSlug):

    blog = BlogModel.objects.filter(
        writer=request.user,
        slug=blogSlug
    ).first()

    if request.method == 'POST':
        form = forms.BlogForm(request.POST, request.FILES or None, instance=blog)

        if form.is_valid():

            form.save()
            
            if blog.is_publish and not blog.is_emailed:

                #TODO send shared email 

                emails = NewsLetterEmailsModel.objects.all().values('email')

                mail_subject = _('بیمارستان موسی ابن جعفر - پست جدید')
                messagee = render_to_string('panel/email-templates/new-blog.html', {
                    'blog': blog,
                    'domain': get_current_site(request).domain,
                })
                
                msg_EMAIL = EmailMessage(
                    mail_subject, messagee, from_email=settings.EMAIL_HOST_USER, to=emails
                )
                msg_EMAIL.content_subtype = "html"
                # msg_EMAIL.send()

                blog.is_emailed = True
                blog.save()

            messages.success(request, _('بلاگ با موفقیت ویرایش شد.'))
            return redirect('panel:blog-list')

    else:
        form = forms.BlogForm(instance=blog)

    return render(request, 'panel/blog/edit.html', {
        'form': form
    })


# url: /panel/blog/tag/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url='/403')
def blog_tag_page(request):

    if request.method == 'POST':
        form = forms.TagForm(request.POST, request.FILES or None)

        if form.is_valid():
            form.save()
            messages.success(request, _('عنوان تگ با موفقیت ذخیره شد.'))
            return redirect('panel:blog-tag')

    else:
        form = forms.TagForm()

    return render(request, 'panel/blog/tag.html', {
        'tags': TagModel.objects.all(),
        'form': form
    })


# url: /panel/blog/category/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url='/403')
def blog_category_page(request):

    if request.method == 'POST':
        form = forms.CategoryForm(request.POST, request.FILES or None)

        if form.is_valid():
            form.save()
            messages.success(request, _('عنوان دسته بندی با موفقیت ذخیره شد.'))
            return redirect('panel:blog-category')

    else:
        form = forms.CategoryForm()

    return render(request, 'panel/blog/category.html', {
        'categories': CategoryModel.objects.all(),
        'form': form
    })


# url: /panel/blog/gallery/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url='/403')
def blog_gallery_page(request):

    if request.method == 'POST':
        form = forms.BlogGalleryForm(request.POST, request.FILES or None)

        if form.is_valid():
            form.save()
            messages.success(request, _('گالری پست با موفقیت ذخیره شد.'))
            return redirect('panel:blog-gallery')

    else:
        form = forms.BlogGalleryForm()

    return render(request, 'panel/blog/gallery.html', {
        'galleries': BlogGalleryModel.objects.all(),
        'form': form
    })