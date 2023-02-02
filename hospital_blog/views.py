from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views import generic
from django.utils.translation import get_language
from .models import (
    BlogModel, BlogCommentModel, BlogLikeModel
)
from . import forms
from extentions.utils import get_client_ip


# url: /blog/list/
class ListPage(generic.ListView):
    template_name = 'blog/list.html'
    model = BlogModel
    paginate_by = 1

    def get_queryset(self):
        blogs = None
        query_search = self.request.GET.get('query')
        
        if query_search:
            lookup = Q(title_fa__icontains=query_search) | Q(title_en__icontains=query_search) | Q(title_ar__icontains=query_search) | Q(title_ru__icontains=query_search)
            blogs = BlogModel.objects.filter(lookup, is_publish=True).distinct()[:6]

        else:
            blogs = BlogModel.objects.filter(is_publish=True).all()[:6]

        blogs_comments = []
        for blog in blogs:
            blogs_comments.append({
                'blog': blog,
                'num_comments': blog.blogcommentmodel_set.filter(is_show=True).count()
            })
        return blogs_comments


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
            return redirect(f'/{get_language()}/blog/info/{blogSlug}/')

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


# url: /blog/search/tags/<query>/
class SearchTag(generic.ListView):
    template_name = 'blog/list.html'
    model = BlogModel
    paginate_by = 1

    def get_queryset(self):

        lang = get_language()
        query = self.kwargs.get('query')
        blogs = []
        
        if lang == 'fa':
            blogs = BlogModel.objects.filter(tags__title_fa=query, is_publish=True).distinct()
        elif lang == 'en':
            blogs = BlogModel.objects.filter(tags__title_en=query, is_publish=True).distinct()
        elif lang == 'ar':
            blogs = BlogModel.objects.filter(tags__title_ar=query, is_publish=True).distinct()
        elif lang == 'ru':
            blogs = BlogModel.objects.filter(tags__title_ru=query, is_publish=True).distinct()

        blogs_comments = []
        for blog in blogs:
            counter = blog.blogcommentmodel_set.filter(is_show=True).count()
            blogs_comments.append({
                'blog': blog, 
                'num_comments': counter
            })
        return blogs_comments


# url: /blog/search/categories/<query>/
class SearchCategory(generic.ListView):
    template_name = 'blog/list.html'
    model = BlogModel
    paginate_by = 1

    def get_queryset(self):

        lang = get_language()
        query = self.kwargs.get('query')
        blogs = []
        
        if lang == 'fa':
            blogs = BlogModel.objects.filter(categories__title_fa=query, is_publish=True).distinct()
        elif lang == 'en':
            blogs = BlogModel.objects.filter(categories__title_en=query, is_publish=True).distinct()
        elif lang == 'ar':
            blogs = BlogModel.objects.filter(categories__title_ar=query, is_publish=True).distinct()
        elif lang == 'ru':
            blogs = BlogModel.objects.filter(categories__title_ru=query, is_publish=True).distinct()

        blogs_comments = []
        for blog in blogs:
            counter = blog.blogcommentmodel_set.filter(is_show=True).count()
            blogs_comments.append({
                'blog': blog, 
                'num_comments': counter
            })
        return blogs_comments

