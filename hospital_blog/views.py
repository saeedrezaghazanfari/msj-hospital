from django.shortcuts import render, get_object_or_404
from .models import (
    BlogModel
)


# url: /blog/blogs/
def list_page(request):
    blogs = BlogModel.objects.filter(
        is_publish=True,
    ).all()[:6]

    return render(request, 'blog/list.html', {
        'blogs': blogs
    })


# url: /blog/blogs/<blogSlug>/
def info_page(request, blogSlug):
    blog = get_object_or_404(BlogModel, slug=blogSlug)

    return render(request, 'blog/info.html', {
        'blog': blog
    })