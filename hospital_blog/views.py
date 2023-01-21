from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views import generic
from .models import (
    BlogModel, BlogCommentModel, BlogLikeModel, CategoryModel
)
from . import forms
from extentions.utils import get_client_ip

# url: /blog/list/
class ListPage(generic.ListView):
    template_name = 'blog/list.html'
    model = BlogModel

    def get_queryset(self):
        blogs = BlogModel.objects.filter(is_publish=True).all()[:6]
        blogs_comments = []
        for blog in blogs:
            comments = BlogCommentModel.objects.filter(blog=blog, reply__isnull=True, is_show=True).count()
            replies = BlogCommentModel.objects.filter(blog=blog, reply__isnull=False, is_show=True).count()
            blogs_comments.append({
                'blog': blog,
                'num_comments': comments + replies
            })
        return blogs_comments
    paginate_by = 1


# url: /blog/info/<blogSlug>/
def info_page(request, blogSlug):

    blog = get_object_or_404(BlogModel, slug=blogSlug, is_publish=True)
    blog_comments = BlogCommentModel.objects.filter(blog=blog, reply__isnull=True, is_show=True).all()
    blog_replies = BlogCommentModel.objects.filter(blog=blog, reply__isnull=False, is_show=True).all()

    # find related blogs
    blog_cateogries = blog.categories.iterator()
    categories_arr_titles = []
    categories_arr = []
    other_blogs = []
    for item in blog_cateogries:
        if not item.title in categories_arr_titles:
            categories_arr_titles.append(item.title)
            categories_arr.append(item)
    for item in categories_arr:
        for find_blog in item.blogmodel_set.all():
            if not find_blog in other_blogs:
                other_blogs.append(find_blog)
    other_blogs.remove(blog)

    if request.method == 'POST':
        form = forms.BlogCommentForm(request.POST or None)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            
            if form.cleaned_data.get('comment_id'):
                comment.reply = get_object_or_404(BlogCommentModel, id=form.cleaned_data.get('comment_id'))
                messages.success(request, _('پاسخ شما ثبت شد. بعد از تایید در سایت نمایش داده خواهد شد. ممنون از حمایت و دلگرمی شما!'))
            else:
                messages.success(request, _('نظر شما ثبت شد. بعد از تایید در سایت نمایش داده خواهد شد. ممنون از حمایت و دلگرمی شما!'))

            comment.save()
            return redirect(f'/blog/info/{blogSlug}/')

    else:
        form = forms.BlogCommentForm()

    return render(request, 'blog/info.html', {
        'blog': blog,
        'other_blogs': other_blogs,
        'form': form,
        'comments': blog_comments,
        'replies': blog_replies,
        'comment_nums': blog_comments.count() + blog_replies.count(),
        'likes': BlogLikeModel.objects.filter(blog=blog, like_dislike='like').count(),
        'dislikes': BlogLikeModel.objects.filter(blog=blog, like_dislike='dislike').count(),
    })


# url: /blog/like-dislike/
@csrf_exempt
def like_dislike_page(request):

    if request.method == 'POST':
        slug = request.POST.get('slug')
        mission_type = request.POST.get('type')

        if not slug.isdigit() or len(str(slug)) != 11:
            return JsonResponse({'status': 400})

        if not mission_type in ['like', 'dislike']:
            return JsonResponse({'status': 400})

        client_ip = get_client_ip(request)

        blog = get_object_or_404(BlogModel, slug=slug, is_publish=True)

        if blog.is_likeable and blog.bloglikemodel_set.filter(user_ip=client_ip).exists():

            blog_feeling = blog.bloglikemodel_set.get(user_ip=client_ip)
            if blog_feeling.like_dislike != mission_type:
                blog_feeling.like_dislike = mission_type
                blog_feeling.save()

            return JsonResponse({
                'type': mission_type, 
                'slug': slug, 
                'likes': BlogLikeModel.objects.filter(blog=blog, like_dislike='like').count(), 
                'dislikes': BlogLikeModel.objects.filter(blog=blog, like_dislike='dislike').count(), 
                'status': 200,
            })

        elif blog.is_likeable and not blog.bloglikemodel_set.filter(user_ip=client_ip).exists():
            blog.bloglikemodel_set.create(user_ip=client_ip, like_dislike=mission_type)
            
            return JsonResponse({
                'type': mission_type, 
                'slug': slug, 
                'likes': BlogLikeModel.objects.filter(blog=blog, like_dislike='like').count(), 
                'dislikes': BlogLikeModel.objects.filter(blog=blog, like_dislike='dislike').count(), 
                'status': 200,
            })

        return JsonResponse({'status': 400})
    return JsonResponse({'status': 400})