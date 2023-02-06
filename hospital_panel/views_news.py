from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from hospital_news.models import NewsModel, NewsGalleryModel, NewsCommentModel
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from hospital_blog.models import TagModel, CategoryModel
from hospital_news.forms import NewsReplyForm, NewsCommentEditForm
from hospital_setting.models import NewsLetterEmailsModel
from extentions.utils import write_action
from .decorators import news_required
from . import forms
 

# url: /panel/news/
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_page(request):

    unpub_news = NewsModel.objects.filter(
        writer=request.user,
        is_publish=False,
    ).all()

    news = NewsModel.objects.filter(
        writer=request.user,
    ).all()

    return render(request, 'panel/news/home.html', {
        'unpub_news': unpub_news,
        'news': news,
    })


# url: /panel/news/create/
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_create_page(request):

    if request.method == 'POST':
        form = forms.NewsForm(request.POST, request.FILES or None)

        if form.is_valid():
            news = form.save(commit=False)
            news.writer = request.user
            news.save()
            form.save_m2m()
            write_action(f'{request.user.username} User created a News.', 'USER')

            if news.is_publish and not news.is_emailed:

                #TODO send shared email 

                emails = NewsLetterEmailsModel.objects.all().values('email')

                mail_subject = _('بیمارستان موسی ابن جعفر - پست جدید')
                messagee = render_to_string('panel/email-templates/new-news.html', {
                    'news': news,
                    'domain': get_current_site(request).domain,
                })
                
                msg_EMAIL = EmailMessage(
                    mail_subject, messagee, from_email=settings.EMAIL_HOST_USER, to=emails
                )
                msg_EMAIL.content_subtype = "html"
                # msg_EMAIL.send()

                news.is_emailed = True
                news.save()

            messages.success(request, _('خبر با موفقیت ویرایش شد.'))
            return redirect('panel:news-list')

    else:
        form = forms.NewsForm()

    return render(request, 'panel/news/create.html', {
        'form': form
    })


# url: /panel/news/edit/<newsSlug>/
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_edit_page(request, newsSlug):

    news = NewsModel.objects.filter(
        writer=request.user,
        slug=newsSlug
    ).first()

    if request.method == 'POST':
        form = forms.NewsForm(request.POST, request.FILES or None, instance=news)

        if form.is_valid():

            form.save()
            write_action(f'{request.user.username} User edited a News.', 'USER')
            
            if news.is_publish and not news.is_emailed:

                #TODO send shared email 

                emails = NewsLetterEmailsModel.objects.all().values('email')

                mail_subject = _('بیمارستان موسی ابن جعفر - خبر جدید')
                messagee = render_to_string('panel/email-templates/new-news.html', {
                    'news': news,
                    'domain': get_current_site(request).domain,
                })
                
                msg_EMAIL = EmailMessage(
                    mail_subject, messagee, from_email=settings.EMAIL_HOST_USER, to=emails
                )
                msg_EMAIL.content_subtype = "html"
                # msg_EMAIL.send()

                news.is_emailed = True
                news.save()

            messages.success(request, _('خبر با موفقیت ویرایش شد.'))
            return redirect('panel:news-list')

    else:
        form = forms.NewsForm(instance=news)

    return render(request, 'panel/news/edit.html', {
        'form': form,
        'news': news
    })


# url: /panel/news/tag/
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_tag_page(request):

    if request.method == 'POST':
        form = forms.TagForm(request.POST or None)

        if form.is_valid():
            form.save()
            write_action(f'{request.user.username} User created a Tag in news panel.', 'USER')
            messages.success(request, _('عنوان تگ با موفقیت ذخیره شد.'))
            return redirect('panel:news-tag')

    else:
        form = forms.TagForm()

    return render(request, 'panel/news/tag.html', {
        'tags': TagModel.objects.all(),
        'form': form
    })


# url: /panel/news/category/
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_category_page(request):

    if request.method == 'POST':
        form = forms.CategoryForm(request.POST or None)

        if form.is_valid():
            form.save()
            write_action(f'{request.user.username} User created a Category in news panel.', 'USER')
            messages.success(request, _('عنوان دسته بندی با موفقیت ذخیره شد.'))
            return redirect('panel:news-category')

    else:
        form = forms.CategoryForm()

    return render(request, 'panel/news/category.html', {
        'categories': CategoryModel.objects.all(),
        'form': form
    })


# url: /panel/news/gallery/
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_gallery_page(request):

    if request.method == 'POST':
        form = forms.NewsGalleryForm(request.POST, request.FILES or None)

        if form.is_valid():

            form.save()
            write_action(f'{request.user.username} User created a news Gallery.', 'USER')
            messages.success(request, _('گالری پست با موفقیت ذخیره شد.'))
            return redirect('panel:news-gallery')

    else:
        form = forms.NewsGalleryForm()

    return render(request, 'panel/news/gallery.html', {
        'galleries': NewsGalleryModel.objects.all(),
        'form': form
    })


# url: /panel/news/comment/
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_comment_page(request):

    if request.method == 'POST':
        form = NewsReplyForm(request.POST or None)

        if form.is_valid():

            that_comment = get_object_or_404(NewsCommentModel, id=form.cleaned_data.get('comment_id'))
            that_news = get_object_or_404(NewsModel, slug=form.cleaned_data.get('news_slug'))

            comment = form.save(commit=False)
            comment.first_name = request.user.firstname()
            comment.last_name = request.user.lastname()
            comment.phone = request.user.phone
            comment.reply = that_comment
            comment.news = that_news
            comment.is_read = True
            comment.is_show = True
            
            comment.save()
            write_action(f'{request.user.username} User sent a Reply in News panel.', 'USER')

            comment.reply.is_read = True
            comment.reply.is_show = True
            comment.reply.save()

            # TODO send sms: send message to comment.reply.phone

            messages.success(request, _('پاسخ شما با موفقیت ثبت شد.'))
            return redirect('panel:news-comments')

    else:
        form = NewsReplyForm()

    return render(request, 'panel/news/comment.html', {
        'form': form,
        'unread_comments': NewsCommentModel.objects.filter(news__writer=request.user, is_read=False).all(),
        'unshow_comments': NewsCommentModel.objects.filter(news__writer=request.user, is_show=False).all(),
    })


# url: /panel/news/comment/read/<commentId>/
@csrf_exempt
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_comment_read_page(request, commentId):

    comment = get_object_or_404(NewsCommentModel, id=commentId, is_read=False)
    comment.is_read = True
    comment.save()
    return redirect('panel:news-comments')


# url: /panel/news/comment/show/<commentId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_comment_show_page(request, commentId):

    comment = get_object_or_404(NewsCommentModel, id=commentId, is_show=False)
    comment.is_show = True
    comment.is_read = True
    comment.save()
    return redirect('panel:news-comments')


# url: /panel/news/comment/delete/<commentId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_comment_delete_page(request, commentId):

    comment = get_object_or_404(NewsCommentModel, id=commentId, is_show=False)
    comment.delete()
    write_action(f'{request.user.username} User Deleted a comment of users in News panel.', 'USER')

    return redirect('panel:news-comments')


# url: /panel/news/comment/edit/<commentId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@news_required(login_url=f'/{get_language()}/403')
def news_comment_edit_page(request, commentId):

    comment = get_object_or_404(NewsCommentModel, id=commentId, is_show=False)

    if request.method == 'POST':
        form = NewsCommentEditForm(request.POST or None, instance=comment)

        if form.is_valid():
            comment = form.save()
            comment.is_show = True
            comment.is_read = True
            
            comment.save()
            write_action(f'{request.user.username} User Edited a comment of users in News panel.', 'USER')

            messages.success(request, _('کامنت کاربر با موفقیت ویرایش شد.'))
            return redirect('panel:news-comments')
    else:
        form = NewsCommentEditForm(instance=comment)

    return render(request, 'panel/news/comment-edit.html', {
        'form': form,
        'comment': comment,
    })