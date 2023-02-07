from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from hospital_blog.models import BlogModel
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from hospital_blog.models import (
    TagModel, CategoryModel, BlogGalleryModel, BlogCommentModel, PampheletModel
)
from hospital_setting.models import NewsLetterEmailsModel
from hospital_blog.forms import BlogReplyForm, BlogCommentEditForm
from extentions.utils import write_action
from .decorators import blog_required
from . import forms
 

# url: /panel/blog/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url=f'/{get_language()}/403')
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
@blog_required(login_url=f'/{get_language()}/403')
def blog_create_page(request):

    if request.method == 'POST':
        form = forms.BlogForm(request.POST, request.FILES or None)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.writer = request.user

            blog.save()
            form.save_m2m()

            write_action(f'{request.user.username} User created a Blog. blogSlug: {blog.slug}', 'USER')

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
        form = forms.BlogForm()

    return render(request, 'panel/blog/create.html', {
        'form': form
    })


# url: /panel/blog/edit/<blogSlug>/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url=f'/{get_language()}/403')
def blog_edit_page(request, blogSlug):

    blog = BlogModel.objects.filter(
        writer=request.user,
        slug=blogSlug
    ).first()

    if request.method == 'POST':
        form = forms.BlogForm(request.POST, request.FILES or None, instance=blog)

        if form.is_valid():

            form.save()
            write_action(f'{request.user.username} User edited a Blog. blogSlug: {blogSlug}', 'USER')
            
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
        'form': form,
        'blog': blog
    })


# url: /panel/blog/tag/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url=f'/{get_language()}/403')
def blog_tag_page(request):

    if request.method == 'POST':
        form = forms.TagForm(request.POST or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User created a Tag in blog panel. tagTitle: {obj.title_fa}', 'USER')
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
@blog_required(login_url=f'/{get_language()}/403')
def blog_category_page(request):

    if request.method == 'POST':
        form = forms.CategoryForm(request.POST or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User created a Category in blog panel. categoryTitle: {obj.title_fa}', 'USER')
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
@blog_required(login_url=f'/{get_language()}/403')
def blog_gallery_page(request):

    if request.method == 'POST':
        form = forms.BlogGalleryForm(request.POST, request.FILES or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User created a blog Gallery. galleryId: {obj.id}', 'USER')

            messages.success(request, _('گالری پست با موفقیت ذخیره شد.'))
            return redirect('panel:blog-gallery')

    else:
        form = forms.BlogGalleryForm()

    return render(request, 'panel/blog/gallery.html', {
        'galleries': BlogGalleryModel.objects.all(),
        'form': form
    })


# url: /panel/blog/comment/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url=f'/{get_language()}/403')
def blog_comment_page(request):

    if request.method == 'POST':
        form = BlogReplyForm(request.POST or None)

        if form.is_valid():

            that_comment = get_object_or_404(BlogCommentModel, id=form.cleaned_data.get('comment_id'))
            that_blog = get_object_or_404(BlogModel, slug=form.cleaned_data.get('blog_slug'))

            comment = form.save(commit=False)
            comment.first_name = request.user.firstname()
            comment.last_name = request.user.lastname()
            comment.phone = request.user.phone
            comment.reply = that_comment
            comment.blog = that_blog
            comment.is_read = True
            comment.is_show = True
            
            comment.save()
            write_action(f'{request.user.username} User sent a Reply in Blog panel. blogSlug: {comment.blog.slug} commentId: {comment.id}', 'USER')

            comment.reply.is_read = True
            comment.reply.is_show = True
            comment.reply.save()

            # TODO send sms: send message to comment.reply.phone

            messages.success(request, _('پاسخ شما با موفقیت ثبت شد.'))
            return redirect('panel:blog-comments')

    else:
        form = BlogReplyForm()

    return render(request, 'panel/blog/comment.html', {
        'form': form,
        'unread_comments': BlogCommentModel.objects.filter(blog__writer=request.user, is_read=False).all(),
        'unshow_comments': BlogCommentModel.objects.filter(blog__writer=request.user, is_show=False).all(),
    })


# url: /panel/blog/pamphlet/
@csrf_exempt
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url=f'/{get_language()}/403')
def blog_pamphlet_page(request):

    if request.method == 'POST':
        form = forms.PampheletForm(request.POST, request.FILES or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User created a pamphlet in Blog panel. pamphletId: {obj.id}', 'USER')
            messages.success(request, _('پمفلت آموزشی شما با موفقیت ثبت شد.'))
            return redirect('panel:blog-pamphlet')

    else:
        form = forms.PampheletForm()

    return render(request, 'panel/blog/pamphlet.html', {
        'form': form,
        'pamphlets': PampheletModel.objects.all(),
    })


# url: /panel/blog/comment/read/<commentId>/
@csrf_exempt
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url=f'/{get_language()}/403')
def blog_comment_read_page(request, commentId):

    comment = get_object_or_404(BlogCommentModel, id=commentId, is_read=False)
    comment.is_read = True
    comment.save()
    return redirect('panel:blog-comments')


# url: /panel/blog/comment/show/<commentId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url=f'/{get_language()}/403')
def blog_comment_show_page(request, commentId):

    comment = get_object_or_404(BlogCommentModel, id=commentId, is_show=False)
    comment.is_show = True
    comment.is_read = True
    comment.save()
    return redirect('panel:blog-comments')


# url: /panel/blog/comment/delete/<commentId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url=f'/{get_language()}/403')
def blog_comment_delete_page(request, commentId):

    comment = get_object_or_404(BlogCommentModel, id=commentId, is_show=False)
    comment.delete()
    write_action(f'{request.user.username} User Deleted a comment of users in Blog panel. commentId: {commentId}', 'USER')
    return redirect('panel:blog-comments')


# url: /panel/blog/comment/edit/<commentId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@blog_required(login_url=f'/{get_language()}/403')
def blog_comment_edit_page(request, commentId):

    comment = get_object_or_404(BlogCommentModel, id=commentId, is_show=False)

    if request.method == 'POST':
        form = BlogCommentEditForm(request.POST or None, instance=comment)

        if form.is_valid():
            comment = form.save()
            comment.is_show = True
            comment.is_read = True

            comment.save()
            write_action(f'{request.user.username} User Edited a comment of users in Blog panel. commentId: {commentId}', 'USER')

            messages.success(request, _('کامنت کاربر با موفقیت ویرایش شد.'))
            return redirect('panel:blog-comments')
    else:
        form = BlogCommentEditForm(instance=comment)

    return render(request, 'panel/blog/comment-edit.html', {
        'form': form,
        'comment': comment,
    })