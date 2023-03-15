from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views import generic
from django.utils.translation import get_language
from hospital_extentions.utils import get_client_ip, write_action
from .models import (
    NewsModel, NewsCommentModel, NewsLikeModel
)
from . import forms


# url: /news/list/
class ListPage(generic.ListView):
    template_name = 'news/list.html'
    model = NewsModel
    paginate_by = 1

    def get_queryset(self):

        query_search = self.request.GET.get('query')
        news = False
        
        if query_search:
            lookup = Q(title_fa__icontains=query_search) | Q(title_en__icontains=query_search) | Q(title_ar__icontains=query_search) | Q(title_ru__icontains=query_search)
            news = NewsModel.objects.filter(lookup, is_publish=True).distinct()[:6]

        else:
            news = NewsModel.objects.filter(is_publish=True).all()[:6]

        news_comments = []
        for item in news:
            news_comments.append({
                'news': item,
                'num_comments': item.newscommentmodel_set.filter(is_show=True).count()
            })
        return news_comments


# url: /news/info/<newsSlug>/
def info_page(request, newsSlug):

    news = get_object_or_404(NewsModel, slug=newsSlug, is_publish=True)
    news_comments = NewsCommentModel.objects.filter(news=news, reply__isnull=True, is_show=True).all()
    news_replies = NewsCommentModel.objects.filter(news=news, reply__isnull=False, is_show=True).all()

    # find related news
    news_cateogries = news.categories.iterator()
    categories_arr_titles = []
    categories_arr = []
    other_news = []
    for item in news_cateogries:
        if not item.title in categories_arr_titles:
            categories_arr_titles.append(item.title)
            categories_arr.append(item)
    for item in categories_arr:
        for find_news in item.newsmodel_set.all():
            if not find_news in other_news:
                other_news.append(find_news)
    other_news.remove(news)

    if request.method == 'POST':
        form = forms.NewsCommentForm(request.POST or None)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            
            if form.cleaned_data.get('comment_id'):
                comment.reply = get_object_or_404(NewsCommentModel, id=form.cleaned_data.get('comment_id'))
                messages.success(request, _('پاسخ شما ثبت شد. بعد از تایید در سایت نمایش داده خواهد شد. ممنون از حمایت و دلگرمی شما!'))
            else:
                messages.success(request, _('نظر شما ثبت شد. بعد از تایید در سایت نمایش داده خواهد شد. ممنون از حمایت و دلگرمی شما!'))

            comment.save()
            write_action(f'user via {comment.phone} phone sent a comment for a News. newsSlug: {comment.news.slug} newsId: {news.id}', 'ANONYMOUS')
            return redirect(f'/news/info/{newsSlug}/')

    else:
        form = forms.NewsCommentForm()

    return render(request, 'news/info.html', {
        'news': news,
        'other_news': other_news,
        'form': form,
        'comments': news_comments,
        'replies': news_replies,
        'comment_nums': news_comments.count() + news_replies.count(),
        'likes': NewsLikeModel.objects.filter(news=news, like_dislike='like').count(),
        'dislikes': NewsLikeModel.objects.filter(news=news, like_dislike='dislike').count(),
    })


# url: /news/like-dislike/
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

        news = get_object_or_404(NewsModel, slug=slug, is_publish=True)

        if news.is_likeable and news.newslikemodel_set.filter(user_ip=client_ip).exists():

            news_feeling = news.newslikemodel_set.get(user_ip=client_ip)
            if news_feeling.like_dislike != mission_type:
                news_feeling.like_dislike = mission_type

                news_feeling.save()
                write_action(f'user via {news_feeling.user_ip} IP {news_feeling.like_dislike}d a News. newsSlug: {news.slug}', 'ANONYMOUS')

            return JsonResponse({
                'type': mission_type, 
                'slug': slug, 
                'likes': NewsLikeModel.objects.filter(news=news, like_dislike='like').count(), 
                'dislikes': NewsLikeModel.objects.filter(news=news, like_dislike='dislike').count(), 
                'status': 200,
            })

        elif news.is_likeable and not news.newslikemodel_set.filter(user_ip=client_ip).exists():
            news.newslikemodel_set.create(user_ip=client_ip, like_dislike=mission_type)
            
            return JsonResponse({
                'type': mission_type, 
                'slug': slug, 
                'likes': NewsLikeModel.objects.filter(news=news, like_dislike='like').count(), 
                'dislikes': NewsLikeModel.objects.filter(news=news, like_dislike='dislike').count(), 
                'status': 200,
            })

        return JsonResponse({'status': 400})
    return JsonResponse({'status': 400})


# url: /news/search/tags/<query>/
class SearchTag(generic.ListView):
    template_name = 'news/list.html'
    model = NewsModel
    paginate_by = 1

    def get_queryset(self):

        lang = get_language()
        query = self.kwargs.get('query')
        news = []
        
        if lang == 'fa':
            news = NewsModel.objects.filter(tags__title_fa=query, is_publish=True).distinct()
        elif lang == 'en':
            news = NewsModel.objects.filter(tags__title_en=query, is_publish=True).distinct()
        elif lang == 'ar':
            news = NewsModel.objects.filter(tags__title_ar=query, is_publish=True).distinct()
        elif lang == 'ru':
            news = NewsModel.objects.filter(tags__title_ru=query, is_publish=True).distinct()

        news_comments = []
        for item in news:
            counter = item.newscommentmodel_set.filter(is_show=True).count()
            news_comments.append({
                'news': item, 
                'num_comments': counter
            })
        return news_comments


# url: /news/search/categories/<query>/
class SearchCategory(generic.ListView):
    template_name = 'news/list.html'
    model = NewsModel
    paginate_by = 1

    def get_queryset(self):

        lang = get_language()
        query = self.kwargs.get('query')
        news = []
        
        if lang == 'fa':
            news = NewsModel.objects.filter(categories__title_fa=query, is_publish=True).distinct()
        elif lang == 'en':
            news = NewsModel.objects.filter(categories__title_en=query, is_publish=True).distinct()
        elif lang == 'ar':
            news = NewsModel.objects.filter(categories__title_ar=query, is_publish=True).distinct()
        elif lang == 'ru':
            news = NewsModel.objects.filter(categories__title_ru=query, is_publish=True).distinct()

        news_comments = []
        for item in news:
            counter = item.newscommentmodel_set.filter(is_show=True).count()
            news_comments.append({
                'news': item, 
                'num_comments': counter
            })
        return news_comments

