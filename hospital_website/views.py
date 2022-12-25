from django.shortcuts import render, redirect


# url: /
def home_page(request):
    return render(request, 'web/home.html', {})
