from django.shortcuts import render
from .models import (
    BlogModel
)


# url: /blog/blogs/
def list_page(request):
    blogs = BlogModel.objects.filter(
        is_publish=True,
        is_activate=True
    ).all()

    return render(request, 'blog/list.html', {
        'blogs': blogs
    })