from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views import generic
from .models import (
    BlogModel, BlogCommentModel, BlogLikeModel, CategoryModel
)
from . import forms
from extentions.utils import safe_string


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